import '../app/globals.css'
import * as React from 'react';
import Button from '@mui/material/Button';
import { useRouter } from 'next/navigation'
import Avatar from '@mui/material/Avatar';
import LogoutIcon from '@mui/icons-material/Logout';

export default function Bar() {
    const router = useRouter()
    const [aviao, setAviao] = React.useState('');
    const logout = ()=>{
        router.push('/access')
    }
    const handleChange = (event) => {
      setAviao(event.target.value);
    };
    function stringToColor(string) {
        let hash = 2;
        let i;
      
        /* eslint-disable no-bitwise */
        for (i = 0; i < string.length; i += 1) {
          hash = string.charCodeAt(i) + ((hash << 5) - hash);
        }
      
        let color = '#';
      
        for (i = 0; i < 3; i += 1) {
          const value = (hash >> (i * 8)) & 0xff;
          color += `00${value.toString(16)}`.slice(-2);
        }
        /* eslint-enable no-bitwise */
      
        return color;
      }
      
    function stringAvatar(name) {
        return {
          sx: {
            bgcolor: stringToColor(name),
          },
          children: `${name.split(' ')[0][0]}${name.split(' ')[1][0]}`,
        };
      }

  return (
    <>
        <div className='flex fixed  h-screen min-w-full'>
            <div className='bg-white bar flex-col p-8 '>
                <div className='flex flex-col justify-around h-full'>
                    <div className='flex flex-col items-center'>
                        <Avatar {...stringAvatar('Ana Nobrega')} />
                        <div className='flex my-4'>
                            <h2>Jhony Klaster</h2> <p className='mx-2'><b>ADM</b></p>
                        </div>
                    </div>
                    <div>
                        <p>
                            <b>Informações Sobre a IA</b>
                        </p>
                        <p>
                            Versão: 0.1
                        </p>
                        <p>
                            acurácia: 80%
                        </p>
                    </div>
                    <Button onClick={logout} className="min-w-full" variant="outlined" color="error"> <p className='mx-4'>Sair</p></Button>
                </div>
            </div>
            
        </div>
    </>
  )
}
//<LogoutIcon />