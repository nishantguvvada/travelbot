"use client"
import { useState, useEffect } from "react";
import toast from 'react-hot-toast';
import axios from "axios";

export const Chat = () => {
    const [userInput, setUserInput] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const [aiResponse, setAIResponse] = useState("");
    const [displayText, setDisplayText] = useState("");
    const [typingIndex, setTypingIndex] = useState(0);
    const [isTyping, setIsTyping] = useState(false);
    const [targetText, setTargetText] = useState("");
    const initialMessage = "Hello, I'm your AI Travel Guide. I help you know about your destination before you travel.";

    // Typing effect controller
    useEffect(() => {
        if (isTyping && typingIndex < targetText.length) {
        const timer = setTimeout(() => {
            setDisplayText(prev => prev + targetText[typingIndex]);
            setTypingIndex(prev => prev + 1);
        }, 20);

        return () => clearTimeout(timer);
        } else {
            setIsTyping(false);
        }
    }, [typingIndex, isTyping, targetText]);

    // Handle text updates
    useEffect(() => {
        if (aiResponse) {
            // Start typing AI response
            setTargetText(aiResponse);
            setDisplayText('');
            setTypingIndex(0);
            setIsTyping(true);
        } else {
            // Start typing initial message
            setTargetText(initialMessage);
            setDisplayText('');
            setTypingIndex(0);
            setIsTyping(true);
        }
    }, [aiResponse]);
  
    const askHandler = async () => {
        setIsLoading(true);
        setAIResponse("");
        try {
            if (userInput == "") {
                setIsLoading(false);
                toast.error("No input provided.")
                return
            }

            const response = await axios.post(`${process.env.NEXT_PUBLIC_BACKEND_URL}/ask`, {
                user_query: userInput
            })

            console.log("response", response.data.response)
            setAIResponse(response.data.response)

            setIsLoading(false);
            toast.success("Response received!")

            // console.log("response:", response);
        } catch(err) {
            console.log("Error: ", err);
            toast.error("Something went wrong.")
            setIsLoading(false);
        }
    }


    return (
        <>
            <div className="mt-2 h-screen w-full flex justify-center">
                <div className="mt-2 w-full mx-4 md:w-[30%]">
                    <div className="w-full p-4 border border-gray-200 bg-gray-50 rounded-t-xl">
                        <div className="grid grid-cols-3">
                            <div className="col-span-3 text-center font-bold h-12">
                                Welcome to travel.ai
                            </div>
                        </div>
                    </div>
                    <div className="w-full h-[40%] p-4 border border-gray-200 bg-white">
                        <div className="grid grid-cols-3">
                            <div className="col-span-3 h-full">
                                {!aiResponse ? 
                                    <p className="mx-2 my-2 font-normal text-gray-500 whitespace-pre-wrap">
                                    {displayText}
                                        {isTyping && (
                                        <span className="ml-1 border-r-2 border-black animate-blink"></span>
                                        )
                                    }
                                    </p> : 
                                    <p className="mx-2 my-2 font-normal text-gray-500 whitespace-pre-wrap">
                                    {displayText}
                                        {isTyping && (
                                        <span className="ml-1 border-r-2 border-black animate-blink"></span>
                                        )
                                    }
                                    </p>
                                }
                            </div>
                        </div>
                    </div>
                    <div className="w-full p-4 border border-gray-200 bg-gray-50 rounded-b-xl">
                        <div className="grid grid-cols-3">
                            <div className="col-span-2">
                                <textarea onChange={(e) => { setUserInput(userInput => e.target.value) }} id="message" rows="4" className="block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500" placeholder="I want to travel to Dubai in July."></textarea>
                            </div>
                            <button onClick={askHandler} className="col-span-1 relative h-full items-center justify-center p-0.5 ml-2 overflow-hidden text-sm font-bold text-white rounded-lg group bg-gradient-to-br from-pink-500 to-orange-400 group-hover:from-purple-600 group-hover:to-blue-500 hover:text-white hover:cursor-pointer dark:text-white focus:ring-4 focus:outline-none focus:ring-blue-300">
                                Send
                            </button>
                            <div role="status" className={`absolute ${!isLoading ? "hidden" : ""} -translate-x-1/2 -translate-y-1/2 top-2/4 left-1/2`}>
                                <svg aria-hidden="true" className="w-8 h-8 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="currentColor"/><path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentFill"/></svg>
                                <span className="sr-only">Loading...</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </>
    )
}