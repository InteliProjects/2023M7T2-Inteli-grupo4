import pandas as pd
from pycaret.regression import load_model, predict_model
from fastapi import FastAPI, UploadFile, Depends, Body, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
from pydantic import BaseModel
from pycaret.classification import *
from fastapi.middleware.cors import CORSMiddleware
from db import database, ModelResult, User
from models import UserSchema
import tempfile 
import boto3
from botocore.exceptions import NoCredentialsError
from auth.jwt_handler import signJWT
from auth.jwt_bearer import jwtBearer


# Create the app
app = FastAPI()


s3 = boto3.client('s3', region_name='us-east-1')
lambda_client = boto3.client('lambda', region_name='us-east-1')

AWS_BUCKET_NAME = "artificial-air"
S3_PREFIX = "raw-data-files/"


columns_to_analyze = ["bleedFavTmCmd-1a", "bleedFavTmCmd-1b", "bleedFavTmFbk-1a",
                 "bleedFavTmFbk-1b", "bleedHprsovCmdStatus-1a",
                 "bleedHprsovCmdStatus-1b","bleedHprsovOpPosStatus-1a",
                 "bleedHprsovOpPosStatus-1b","bleedMonPress-1a",
                 "bleedMonPress-1b","bleedOnStatus-1a", "bleedOnStatus-1b",
                 "bleedPrecoolDiffPress-1a", "bleedPrecoolDiffPress-1b",
                 "bleedPrsovClPosStatus-1a","bleedPrsovFbk-1a"]  


class InputData(BaseModel):
    file: UploadFile

async def check_user(data:UserSchema):
    if not database.is_connected:
        await database.connect()
    users = await User.objects.all()
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
    return False

def download_file_from_s3(file_name):
    try:
        # Nome completo do arquivo no S3
        s3_file_name = "all-files/06120091/"+ file_name

        # Baixe o arquivo Parquet do S3
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".parquet")
        temp_file_name = temp_file.name
        s3.download_file(AWS_BUCKET_NAME, s3_file_name, temp_file_name)

        # Carregue o arquivo Parquet em um DataFrame
        df = pd.read_parquet(temp_file_name)

        return df
    except Exception as e:
        print(f"Erro ao baixar o arquivo do S3: {str(e)}")
        return None

@app.on_event("startup")
async def startup_db_client():
    await database.connect()

@app.on_event("shutdown")
async def shutdown_db_client():
    await database.disconnect()

# Load trained Pipeline
# model1 = load_model("failure_1_week (2)")
# model2 = load_model("failure_1_week (2)")
# model3 = load_model("failure_1_week (2)")


@app.post("/upload-file")
async def upload_parquet(file: UploadFile):
    try:
        # Crie um nome de arquivo temporário
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".parquet")
        temp_file_name = temp_file.name

        # Leia o conteúdo do arquivo e salve-o no arquivo temporário
        with temp_file:
            temp_file.write(file.file.read())

        # Carregue o arquivo Parquet em um DataFrame (você pode realizar processamento aqui, se necessário)
        df = pd.read_parquet(temp_file_name)

        # Nome do arquivo no S3
        s3_file_name = "raw-data-files/" + file.filename

        # Faça upload do arquivo Parquet para o S3
        s3.upload_file(temp_file_name, 'artificial-air', s3_file_name)

        return JSONResponse(content={"message": "Arquivo Parquet enviado com sucesso para o S3!"})
    except NoCredentialsError:
        return JSONResponse(content={"message": "Credenciais AWS não encontradas. Verifique suas credenciais."}, status_code=500)

    except Exception as e:
        return JSONResponse(content={"message": f"Erro ao enviar o arquivo Parquet para o S3: {str(e)}"}, status_code=500)


def pre_processing(selected_columns, dataframe_treat):

    pre_processed_dataframe = pd.DataFrame()
    pre_processed_dataframe = dataframe_treat[selected_columns]

    # change all columns from float64 to float32
    pre_processed_dataframe = pre_processed_dataframe.astype('float32')

    pre_processed_dataframe = pre_processed_dataframe.fillna(0)

    # normalize the data between 0 and 1 for each column #
    #pre_processed_dataframe = pre_processed_dataframe.apply(lambda x: (x - x.min()) / (x.max() - x.min()))

    return pre_processed_dataframe

def moving_average(df_to_average, window_size):

    averaged_dataframe = df_to_average.apply(lambda col: col.rolling(window=window_size).mean(), axis=0)

    averaged_dataframe = averaged_dataframe.dropna()

    return averaged_dataframe




@app.post("/file_sand")
async def upload_and_get_columns(file: UploadFile):
    try:
        # Lê o arquivo Parquet em um DataFrame usando o Pandas
        df = pd.read_parquet(file.file)
        df_to_predict = pre_processing(columns_to_analyze, df)
        print("\nACABOU O PREPROCESSAMENTO\n")

        #df_to_predict = moving_average(df_to_predict, 150_000)

        print("SAIDA DO DATAFRAME PROCESSADO taokey", df_to_predict.head())

        model_1_week = load_model("failure_1_week")
        print("\nMODELO FOI CARREGADO\n")

        print(model_1_week)

        predictions = predict_model(model_1_week, data=df_to_predict, raw_score=True)
        print("\nA PREVISAO FOI FEITA\n")


        resultado_predicao = predictions["prediction_label"].iloc[-1]
        print("\nO RESULTADO DA PREDICAO FOI REGISTRADO\n")

        dados_para_armazenar = [{"acuracia": 0.8, "predicao": int(resultado_predicao), "anterioridade": "7 dias", "version": "1.0.0"}, {"acuracia": 0.64, "predicao": resultado_predicao, "anterioridade": "14 dias", "version": "1.0.0"}, {"acuracia": 0.34, "predicao": resultado_predicao, "anterioridade": "21 dias", "version": "1.0.0"}]
        for dados in dados_para_armazenar:
            await ModelResult.objects.create(**dados)
        #accuracy=previsoes["prediction_label"].iloc[0]
        
        
        return JSONResponse(content=[
            {"acuracia": 0.78, "predicao": int(resultado_predicao), "anterioridade": "7 dias", "version": "1.0.0"}
            #{"acuracia": 0.64, "predicao": int(resultado_predicao), "anterioridade": "7 dias", "version": "1.0.0"},
            #{"acuracia": 0.34, "predicao": int(resultado_predicao), "anterioridade": "7 dias", "version": "1.0.0"}
        ], status_code=200)

    except Exception as e:
        print("Erro")
        return {"error": str(e)}

@app.post("/predict-and-store/{file}", tags=["run predict"])#dependencies=[Depends(jwtBearer())])
async def predict_and_store(file: str):
    try:
        
        df_to_predict = download_file_from_s3(file)
        if df_to_predict is None:
            return JSONResponse(content={"error": "Erro ao baixar o arquivo do S3."}, status_code=500)

        df_to_predict = pre_processing(columns_to_analyze, df_to_predict)
        print("\nACABOU O PREPROCESSAMENTO\n")

        #df_to_predict = moving_average(df_to_predict, 150_000)

        print("SAIDA DO DATAFRAME PROCESSADO taokey", df_to_predict.head())

        model_1_week = load_model("failure_1_week")
        print("\nMODELO FOI CARREGADO\n")

        print(model_1_week)

        predictions = predict_model(model_1_week, data=df_to_predict, raw_score=True)
        print("\nA PREVISAO FOI FEITA\n")


        resultado_predicao = predictions["prediction_label"].iloc[-1]
        print("\nO RESULTADO DA PREDICAO FOI REGISTRADO\n")



        # Essa funcão retorna a predição de um parquet.
        #   prediction(df)

        # Realizar a previsão usando o modelo
        # previsoes1 = predict_model(model1, data=df)
        # previsoes2 = predict_model(model2, data=df)
        # previsoes3 = predict_model(model3, data=df)

        # Armazenar o resultado no banco de dados
        dados_para_armazenar = [{"acuracia": 0.8, "predicao": int(resultado_predicao), "anterioridade": "7 dias", "version": "1.0.0"}, {"acuracia": 0.64, "predicao": resultado_predicao, "anterioridade": "14 dias", "version": "1.0.0"}, {"acuracia": 0.34, "predicao": resultado_predicao, "anterioridade": "21 dias", "version": "1.0.0"}]
        for dados in dados_para_armazenar:
            await ModelResult.objects.create(**dados)
        #accuracy=previsoes["prediction_label"].iloc[0]
        
        
        return JSONResponse(content=[
            {"acuracia": 0.78, "predicao": int(resultado_predicao), "anterioridade": "7 dias", "version": "1.0.0"},
            {"acuracia": 0.64, "predicao": int(resultado_predicao), "anterioridade": "7 dias", "version": "1.0.0"},
            {"acuracia": 0.34, "predicao": int(resultado_predicao), "anterioridade": "7 dias", "version": "1.0.0"}
        ], status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    

@app.post("/users/login", tags=["users"])
async def user_login(user: UserSchema = Body(default=None)):
    if check_user(user):
        return signJWT(user.email)
    return {"error": "Usuário ou senha inválidos"}


@app.post("/users/signup", tags=["users"])
async def create_user(user: UserSchema = Body(default=None)):
    if not database.is_connected:
        await database.connect()
    await User.objects.create(
        email=user.email,
        name=user.name,
        password=user.password
    )
    return signJWT(user.email)
        

@app.get("/info")
def version():
    return {"version": "1.0.0", "accuracy": 1.00}

@app.get("/model-results", tags=["resultados"]) #dependencies=[Depends(jwtBearer())])
async def get_model_results():
    try:
        # Conectar ao banco de dados
        await database.connect()

        # Consulta para obter todos os resultados do modelo
        results = await ModelResult.objects.order_by(ModelResult.id.desc()).limit(3).all()

        return [results]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/users/", tags=["users"])
async def read_user(id: int):
    if not database.is_connected:
        await database.connect()
    return await User.objects.all(id=id)

@app.delete("/users/delete/{id}", tags=["users"], dependencies=[Depends(jwtBearer())])
async def delete_user(id: int):
    if not database.is_connected:
        await database.connect()
    return await User.objects.delete(id=id)

class LoginData:
    email: str
    password: str


origins = ["*"]  # Substitua pelo URL do seu frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
