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

              <FileInput/>
              
            </div>
          </div>
        </div>
      </div>
        
    </main>
    
  );
}



