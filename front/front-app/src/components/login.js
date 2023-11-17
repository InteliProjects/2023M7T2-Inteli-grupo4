
'use client'
 
import '../app/globals.css'
import { useState } from 'react';
import { Box, Button, TextField, Typography } from '@mui/material';
import { useRouter } from 'next/navigation'

const Login = () => {
  const router = useRouter()
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isSubmitted, setIsSubmitted] = useState(false); // Estado para rastrear se o formulário foi enviado
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const handleEmailChange = (e) => {
    setEmail(e.target.value);
  };

  const handlePasswordChange = (e) => {
    setPassword(e.target.value);
  };

  const handleLogin = () => {
    setIsSubmitted(true); // Marca o formulário como enviado

    // Conexão com server
    if (email != '' && password != '') {
        let url = "http://localhost:3000/auth/login";
            const dados = {
                username: String(email),
                password: String(password)
            };
            const configuracao = {
            method: 'POST', // Método HTTP POST
            headers: {
                'Content-Type': 'application/json' // Tipo de conteúdo JSON
            },
            body: JSON.stringify(dados) // Converte os dados em JSON e os envia no corpo da solicitação
            };

            // Fazendo a solicitação POST usando a API Fetch
            fetch(url, configuracao)
            .then(response => {
                if (!response.ok) {
                    setIsLoggedIn(false);
                    throw new Error('Não foi possível completar a requisição.');
                }
                return response.json()
            })
            .then(data =>{
                const authToken = getCookie('authToken');
                console.log(authToken)
                })

      //router.push('/')
      setIsLoggedIn(true);
    } else {
      setIsLoggedIn(false);
    }
  };

  return (
    <div
    >
      <Box
        className="bg-white rounded-lg shadow-md loginCard p-8"
        align="center"
      >
        <Typography variant="h4" align="center" gutterBottom>
          Faça login
        </Typography>
        <TextField
          label="Email"
          fullWidth
          margin="normal"
          variant="outlined"
          value={email}
          onChange={handleEmailChange}
          className="mb-4"
        />
        <TextField
          label="Senha"
          fullWidth
          margin="normal"
          variant="outlined"
          type="password"
          value={password}
          onChange={handlePasswordChange}
          className="mb-6"
        />
        <Button
          variant="outlined"
          color="primary"
          fullWidth
          onClick={handleLogin}
          className="py-3 bg-white border border-gray-500 text-gray-500 hover:bg-blue-500 hover:text-white hover:border-none hover:shadow-md btn_Access"
        >
          Entrar
        </Button>
        {isSubmitted && !isLoggedIn ? (
          <Typography
            variant="body2"
            align="center"
            className="mt-4 text-red-600"
          >
            Credenciais inválidas. Tente novamente.
          </Typography>
        ) : null}
      </Box>
    </div>
  );
};

export default Login;



