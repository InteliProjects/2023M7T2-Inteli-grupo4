'use client'
import '../app/globals.css'
import Bar from "../components/bar"
import React, { useState, useEffect } from 'react';
import FileInput from '../components/FileInput';
import { VictoryBar, VictoryChart, VictoryAxis } from 'victory';



export default function Home() {

  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const handleFileSelect = (file) => {
    // Faça algo com o arquivo selecionado, por exemplo, envie-o para o servidor.
    console.log('Arquivo selecionado:', file);
  };

  useEffect(() => {
    fetch('http://35.173.106.203/model-results') // Substitua pela URL da sua rota Express.js
      .then((response) => response.json())
      .then((result) => {
        setData(result);
        console.log(response)
        setLoading(false);
      })
      .catch((error) => {
        console.error('Erro ao buscar os dados:', error);
        setLoading(false);
      });
  }, []);

  return (
    <main className="min-h-screen">
      <div className='content'> 
        <div className='itemBar'>
          <Bar/>
        </div>
        <div className='itemContent'>
          <div className='flex min-h-screen flex-col justify-center items-center'>
            <div className='bg-white w-9/12 cardPadding h-5/6 rounded-xl'>

                        {loading ? (
                <p>Carregando...</p>
              ) : (
                <div className="w-full">
                  {data.map((data_) => (
                    <div key={0}  className='graphcs'>
                      <VictoryChart
                          // adding the material theme provided with Victory
                          domainPadding={20}
                          >
                          <VictoryAxis
                          tickValues={[1, 2, 3]}
                          tickFormat={["7 Dias", "1 Mês", "3 messe"]}
                          />
                          <VictoryAxis
                          dependentAxis
                          tickFormat={(y) => (`${y}%`)}
                          />
                          <VictoryBar
                          data={data_}
                          x="anterioridade"
                          y="acuracia"
                          />
                      </VictoryChart>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
        
    </main>
    
  );
}



