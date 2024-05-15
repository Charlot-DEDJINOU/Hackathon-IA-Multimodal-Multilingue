import React, { useState } from "react";
import Input from '../components/commons/Input';
import Button from '../components/commons/Button';
import { useNavigate } from 'react-router-dom';

export default function Login() {
    const navigate = useNavigate();
    const [loading, setLoading] = useState(false);

    const handleSubmit = (e) => {
        e.preventDefault()
        setLoading(true)
        navigate('/')
        setLoading(false)
    }
    
    return (
        <section className="w-full bg-white md:bg-blue-50 flex flex-col items-center justify-center pb-7">
            <div className='my-5 flex'>
                <span className='text-3xl text-primary font-bold mx-2'>SMART VT</span>
            </div>
            <div className='p-10 bg-white rounded-md'>
                <p className='text-center font-bold text-2xl text-primary mb-7'>Connexion à votre compte</p>
                <p className='text-center mb-3'>Entrez votre nom d'utilisateur et votre mot de passe pour vous connecter</p>
                <form className='my-7' onSubmit={handleSubmit}>
                    <Input
                        label="Identifiant"
                        type="text"
                        name="identifiant"
                        placeholder="Entrez votre identifiant"
                    />
                    <Input
                        label="Mot de passe"
                        type="password"
                        name="password"
                        placeholder="Entrez votre mot de passe"
                    />
                    <Button className="w-full my-3" isLoading={loading}>Connexion</Button>
                </form>
                <p className='text-center'>Vous n'avez pas de compte ? <span className='hover:cursor-pointer text-primary' onClick={() => navigate('/register')}>Créer un compte</span></p>
            </div>
        </section>
    );
}