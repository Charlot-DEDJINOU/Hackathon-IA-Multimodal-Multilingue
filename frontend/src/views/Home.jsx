import Button from '../components/commons/Button';
import { doublageYoruba, transcribeYoruba } from '../services/pythonServices';
import { getSubtitles } from '../services/nodeServices';
import AlertDanger from "../components/commons/AlertDanger"
import AlertSuccess from "../components/commons/AlertSuccess"
import {useState} from "react";
import Select from "../components/commons/Select"

const VideoUploader = () => {

    const [loading, setLoading] = useState(false);
    const [videoBlob, setVideoBlob] = useState(null);
    const [transBlob, setTransBlob] = useState(null);
    let duration = 0

    const [data, setData] = useState({
        file : '',
        option : '',
        destination : ''
    })

    const [message, setMessage] = useState({
        display : false,
        type : 'success',
        content : ''
    })

    const handleChange = (e) => {
        setData({
            ...data,
            [e.target.name]: e.target.value
        })
    }

    const analyseDuration = () => {
        if(duration > 90){
            setMessage({
                display : true,
                type : 'error',
                content : "Pour le moment updoler une vidéo de - 1 min 30 secondes"
            })
        }
    }

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        setVideoBlob(URL.createObjectURL(new Blob([file], { type: 'video/mp4' })));

        setData({
            ...data,
            [e.target.name] : file
        })

        const reader = new FileReader();
        reader.onload = (event) => {
            const videoElement = document.createElement('video');
            videoElement.src = event.target.result;
            videoElement.onloadedmetadata = () => {
                duration = videoElement.duration;
                analyseDuration()
            };
        };
        reader.readAsDataURL(file);
    };
    

    const handleSubmit = async () => {
        analyseDuration()
        if(duration < 90) {
            setLoading(true);
            
            if(data.destination != 'yoruba'){
                setMessage({
                    display : true,
                    type : 'error',
                    content : "Pour le moment nous supportons que yoruba en destination."
                })
            }else {
                const formData = new FormData()
                let resultVideo = null
                let response = null;
                console.log(data)
                formData.append('video_file', data.file)

                if(data.option == '1') {
                    response = await transcribeYoruba(formData)

                    formData.append('data', JSON.stringify(response))
                    response = await getSubtitles(formData)

                    resultVideo = response.videoUrl
                }else if(data.option == '2' || data.option == '3'){
                    response = await doublageYoruba(formData)

                    resultVideo = response.url_output
                }

                setTransBlob(resultVideo)
            }
        
            setLoading(false);
        }
    };    

    return (
        <section className='bg-white p-7'>
            <p className='text-center mb-5'><span className='font-bold text-2xl text-primary'>SMART VT</span> vous permet de sous-titrer et de doubler n'importe quelle vidéo, quel que soit son langage d'origine, vers n'importe quelle langue de votre choix.</p>
            <div className='flex flex-col'>
                <div className='flex-wrap md:flex-nowrap flex w-full'>
                    <div className='w-full md:w-1/2 p-5 flex items-center justify-center'>
                    {
                        videoBlob && 
                        <video
                            className='w-full h-96'
                            id="video"
                            src={videoBlob}
                            controls
                        >
                        </video>
                    }
                    </div>
                    <div className='w-full md:w-1/2 p-5 flex items-center justify-center'>
                    {
                        !loading ?
                        transBlob ? 
                        <video
                            className='w-full h-96'
                            src={transBlob}
                            controls
                        >
                        </video> : null
                        : <div className="border-gray-300 h-20 w-20 animate-spin rounded-full border-8 border-t-primary" />
                    }
                    </div>
                </div>
                <div className="flex flex-col w-full">   
                    <div className='mb-4'>
                        <label className="mb-3">Choisir la vidéo</label>
                        <input 
                            type="file"
                            name="file"
                            onChange={handleFileChange} 
                            className="block w-full border rounded-md text-sm focus:z-10 border-primary bg-slate-200 focus:outline-none focus:border-primary disabled:opacity-50 disabled:pointer-events-none file:bg-primary file:border-0 file:text-white file:me-4 file:py-3 file:px-4 hover:cursor-pointer" 
                        />
                    </div>
                    <Select label="Options" onChange={handleChange} name="option">
                        <option value="1">Sous titré</option>
                        <option value="2">Doublage</option>
                        <option value="3">Sous titré et Doublage</option>
                    </Select>
                    <Select label="Langue de destination" onChange={handleChange} name="destination">
                        <option value="fon">Fon</option>
                        <option value="français">Français</option>
                        <option value="yoruba">Yoruba</option>
                    </Select>
                    { message.display && message.type === 'error' && <AlertDanger message={message.content} /> }
                    { message.display && message.type === 'success' && <AlertSuccess message={message.content} /> }
                    <Button isLoading={loading} onClick={handleSubmit}>
                        Charger la vidéo
                    </Button>
                </div>
            </div>
        </section>
    );
};

export default VideoUploader;