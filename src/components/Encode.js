import React, { useState } from "react";

export default function Encode() {

    const [textInput, setTextInput] = useState("")
    const [imageInput, setImageInput] = useState()

    const [backendData, setBackendData] = useState()


    function handleEncodeSubmit(event) {
        event.preventDefault()
        const finalData = new FormData()
        finalData.append("file", imageInput)
        finalData.append("message", textInput)

        fetch("/encode_request" ,{
            method: "POST",
            body: finalData,
            'Content-Type': 'mutlipart/form-data'
        })
        .then(res => res.blob())
        .then(blob => setBackendData(URL.createObjectURL(blob)))
    }


    return (
        <form className="encode--inputs" onSubmit={handleEncodeSubmit}>
            <p>Type a message that you would like to encode. Then select the image that you want the message to be encoded in</p>
            <textarea 
                className="encode--message--input" 
                id="text" name="text--input" 
                rows="5" 
                cols="33" 
                placeholder="Input Message"
                value={textInput}
                onChange={(event) => setTextInput(event.target.value)}> 
             </textarea>

             <input
                    type="file"
                    accept="image/*"
                    name="file"
                    onChange={(event) => setImageInput(event.target.files[0])}
            />

            <button 
                className="photo--select--button button" 
                id="select"
                onClick={() => console.log(imageInput)}>
                Submit
            </button>

            <img src={backendData} alt="uploaded"/>

        </form>
    )
}