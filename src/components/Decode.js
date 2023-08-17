import React, { useState } from "react";

export default function Decode() {

    const [imageInput, setImageInput] = React.useState()
    const [backendData, setBackendData] = React.useState()

    let message_received = false

    function handleDecodeSubmit(event) {
        event.preventDefault()
        const finalData = new FormData()
        finalData.append("file", imageInput)

        fetch("/decode_request" ,{
            method: "POST",
            body: finalData,
            'Content-Type': 'mutlipart/form-data'
        })
        .then(res => res.json())
        .then(data => setBackendData(data.message))
        
        message_received = true
    }

    return (
        <form className="decode--inputs" onSubmit={handleDecodeSubmit}>
            <h3 className="decode--inputs--text">Select the photo you want to decode</h3>
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

            <h3>The decoded message is: {backendData}</h3>

        </form>
    )
}