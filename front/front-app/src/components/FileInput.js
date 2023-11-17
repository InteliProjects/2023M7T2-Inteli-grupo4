import React, { useState } from 'react';
import { Button, Alert, Stack } from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';

function FileInput() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [alertOpen, setAlertOpen] = useState(false);

  const handleFileSelect = async (e) => {
    const file = e.target.files[0];
    setSelectedFile(file);
    if (!file) {
      console.log("Falha no arquivo")
      return;
    }
    const formData = new FormData();
    formData.append('file', file);


    try {
      // URL para a API
      const response = await fetch('http://34.224.207.61/upload-file', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        console.log('Resposta do servidor:', data); 
        console.log('Arquivo enviado com sucesso.');
      } else {
        console.error('Erro ao enviar o arquivo.');
      }
    } catch (error) {
      console.error('Erro na solicitação:', error);
    }
    setAlertOpen(true);
    window. location. reload();
  };

  

  return (
    <div>
      <input
        type="file"
        accept="*" 
        onChange={handleFileSelect}
        style={{ display: 'none' }}
        id="fileInput"
      />
      <label htmlFor="fileInput">
        <Button
          variant="contained"
          component="span"
          style={{ marginLeft: '10%', width: '78%',  marginTop: "10px" }}
          startIcon={<CloudUploadIcon />}
        >
          Escolher Arquivo
        </Button>
      </label>
      {(selectedFile && alertOpen == true) && (
        <Stack style={{marginLeft: '10%', width: '78%'}} spacing={2}>
          <Alert
            onClose={() => {
              setAlertOpen(false);
              setSelectedFile(null);
            }}
            severity="success"
            variant="outlined"
          >
            Arquivo {selectedFile.name} selecionado!
          </Alert>
        </Stack>
      )}
    </div>
  );
}

export default FileInput;
