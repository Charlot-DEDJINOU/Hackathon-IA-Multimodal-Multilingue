import React, { useState } from "react";
import Input from '../components/commons/Input';
import Button from '../components/commons/Button';
import { useNavigate } from 'react-router-dom';

export default function Register() {
    const navigate = useNavigate();

    const [loading, setLoading] = useState(false)
    
    const handleSubmit = (e) => {
        e.preventDefault()
        setLoading(true)
        navigate('/')
        setLoading(false)
    }

    return (
        <section className="w-full bg-white md:bg-blue-50 flex flex-col items-center justify-center pb-7">
            <div className="my-5 flex">
            <span className='text-3xl text-primary font-bold mx-2'>SMART VT</span>
            </div>
            <div className="p-8 bg-white rounded-md sm:w-full md:w-3/4 lg:w-1/2">
                <p className="text-center font-bold text-2xl text-primary mb-7">Inscription</p>
                <form className="my-7" onSubmit={handleSubmit}>
                    <div className="md:flex">
                        <Input
                            label="Nom"
                            name="structure"
                            placeholder="Nom de la Structure"
                            type="text"
                            className="mr-2"
                        />
                        <Input
                            label="Prénom"
                            name="poste"
                            type="text"
                            placeholder="Entrez votre Poste"
                            className="mt-2 md:mt-0"
                        />
                    </div>
                    <Input
                        label="Email"
                        name="identifiant"
                        type="text"
                        placeholder="Entrez votre email"
                    />
                    <div className="md:flex">
                        <Input
                            label="Mot de passe"
                            type="password"
                            name="password"
                            placeholder="Entrez votre mot de passe"
                            className="mr-2"
                        />
                        <Input
                            label="Confirmer Mot de passe"
                            type="password"
                            name="password_verify"
                            className="mt-2 md:mt-0"
                        />
                    </div>
                    <Button className="w-full my-3" isLoading={loading}>Inscription</Button>
                </form>
                <p className="text-center">Vous avez déjà un compte ? <span className="hover:cursor-pointer text-primary" onClick={() => navigate('/')}>Connectez-vous</span></p>
            </div>
        </section>
    );
}