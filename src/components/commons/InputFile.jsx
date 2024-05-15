export default function InputFile({label, className, name}){
    return(
        <div className={`w-full mb-4 flex flex-col ${className}`}>   
            <label className=" mb-2">{ label }</label>
            <input type="file" name={name} className="block w-full border rounded-md text-sm focus:z-10 border-primary bg-slate-200 focus:outline-none focus:border-primary disabled:opacity-50 disabled:pointer-events-none
            file:bg-primary file:border-0 file:text-white file:me-4 file:py-3 file:px-4 hover:cursor-pointer" />
        </div>
    )
}