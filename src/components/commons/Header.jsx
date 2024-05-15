import { Link } from "react-router-dom";

export default function Header(){
    return(
        <header className="w-full h-17 bg-primary flex items-center justify-around">
            <Link to="/" className="font-bold text-xl text-white">SMART VT</Link>
            <div className="w-3/4">
                <ul className="flex items-center justify-end">
                    <li className="mx-4 text-white text-lg font-medium">
                        <Link to="/login">Connexion</Link>
                    </li>
                    <li className="mx-4 text-white text-lg font-medium">
                        <Link to="/register">Inscription</Link>
                    </li>
                </ul>
            </div>
        </header>
    )
}