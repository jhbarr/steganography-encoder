import React, { useState } from "react";

import Encode from "./Encode";
import Decode from "./Decode";

export default function Inputs() {

    const [inputType, setInputType] = useState("")


    return (
        <div>
            <div className="option-buttons">
                <button 
                    className="encode--button option--button" 
                    id="encode"
                    onClick={() => setInputType("encode")}>
                        Encode
                </button>

                <button 
                    className="decode--button option--button" 
                    id="decode"
                    onClick={() => setInputType("decode")}>
                    Decode
                </button>
                {inputType === "" && <h3 className="prompt">Would you like to encode or decode an image?</h3>}
            </div>
            {inputType === "encode" && <Encode />}
            {inputType === "decode" && <Decode />}
        </div>

    )
}