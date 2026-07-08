import Sidebar from "../components/Sidebar";
import { useParams } from "react-router-dom";
import { getFiles, askDocumentAI } from "../services/api";
import { useEffect, useState, useRef } from "react";
import { FiSend } from "react-icons/fi";
function DocumentAI() {
    const { id } = useParams();

    const [document, setDocument] = useState(null);
    const [question, setQuestion] = useState("");
    const [loading, setLoading] = useState(false);
    const [history, setHistory] = useState([]);
    const [messages, setMessages] = useState([]);
    const messagesEndRef = useRef(null);
    const textareaRef = useRef(null);
    useEffect(() => {

        getFiles()
            .then((response) => {

            const file = response.data.find(
                (item) => item.id === Number(id)
            );

            setDocument(file);

            })
            .catch(console.error);

        }, [id]);
    useEffect(() => {
            messagesEndRef.current?.scrollIntoView({
                behavior: "smooth",
            });
        }, [messages, loading]);
        const handleTextareaChange = (e) => {
            setQuestion(e.target.value);

            const textarea = textareaRef.current;

            textarea.style.height = "56px";
            textarea.style.height = `${textarea.scrollHeight}px`;
        };
    const handleAsk = async () => {

        if (!question.trim()) return;

        try {

            setLoading(true);

            const response = await askDocumentAI(
                Number(id),
                question,
                history
            );

            setMessages((prev) => [
                ...prev,
                {
                    role: "user",
                    text: question,
                },
                {
                    role: "assistant",
                    text: response.data.answer,
                    sources: response.data.sources,
                },
                ]);

                setQuestion("");
                if (textareaRef.current) {
                    textareaRef.current.style.height = "56px";
                }

            setHistory([
                ...history,
                {
                    role: "user",
                    text: question,
                },
                {
                    role: "assistant",
                    text: response.data.answer,
                    sources: response.data.sources,
                },
            ]);

        } catch (err) {

            console.error(err);

            setMessages((prev) => [
                ...prev,
                {
                    role: "assistant",
                    text: "Something went wrong.",
                },
                ]);

        } finally {

            setLoading(false);

        }

        };
  return (
    <div className="h-screen overflow-hidden app-bg flex">
  <Sidebar />

  <main className="flex-1 flex flex-col h-screen">
    {/* Header */}
    <div className="border-b border-white/10 app-bg px-10 py-6 shadow-md">
      <h1 className="text-4xl font-bold">
        📄 {document?.name || "Loading..."}
      </h1>

      <p className="text-theme opacity-70 mt-3 break-all">
        {document?.path}
      </p>
    </div>
    {messages.length === 0 && !loading && (

    <div className="flex flex-col items-center justify-center h-full opacity-60">

        <div className="text-6xl">
            📄
        </div>

        <h2 className="mt-6 text-2xl font-semibold">

            Ask anything about this document

        </h2>

        <p className="mt-2">

            AXON will answer using only this document.

        </p>

    </div>

    )}


    {/* Chat Messages */}
    <div className="flex-1 overflow-y-auto px-10 py-6 text-theme">
        <div className="space-y-8">
        {messages.map((msg, index) => (

    <div
        key={index}
        className={`flex flex-col ${
            msg.role === "user" ? "items-end" : "items-start"
        }`}
    >

            <div className="font-semibold mb-2">
                {msg.role === "user" ? "🧑" : "🤖"}
            </div>

        <div
            className={`rounded-3xl px-6 py-4 whitespace-pre-wrap ${
                msg.role === "user"
                    ? "bg-cyan-600 text-white max-w-2xl"
                    : "card-bg max-w-3xl"
            }`}
        >
            {msg.text}

            {msg.role === "assistant" &&
                msg.sources &&
                msg.sources.length > 0 && (
                <div className="mt-4 text-sm">
                    <div className="font-semibold text-cyan-400">
                    📄 Sources
                    </div>

                    <div className="mt-3 space-y-2">

                        {msg.sources.map((source, index) => (

                            <div
                                key={index}
                                className="rounded-xl border border-white/10 bg-black/20 px-4 py-3"
                            >
                                <div className="font-medium">

                                    📄 {source.file}

                                </div>

                                <div className="text-xs opacity-70 mt-1">

                                    Page {source.page}

                                </div>

                            </div>

                        ))}

                    </div>
                                    
                
                </div>
                )}
                
            </div>
            </div>
        ))}
        {loading && (
                <div className="flex flex-col items-start">
                    <div className="font-semibold mb-2">🤖 AXON</div>

                    <div className="card-bg rounded-3xl px-6 py-4 flex gap-2">

                        <span className="w-2 h-2 rounded-full bg-violet-400 animate-bounce"></span>

                        <span
                            className="w-2 h-2 rounded-full bg-violet-400 animate-bounce"
                            style={{ animationDelay: "0.15s" }}
                        ></span>

                        <span
                            className="w-2 h-2 rounded-full bg-violet-400 animate-bounce"
                            style={{ animationDelay: "0.3s" }}
                        ></span>

                    </div>
                </div>
        )}
                <div ref={messagesEndRef}></div>
        
        </div>
    </div>
        {/* AI Input */}
    <div className="border-t border-white/10 app-bg px-10 py-4 shadow-[0_-8px_30px_rgba(0,0,0,0.25)]">

        <div className="flex items-end gap-3">

            <textarea
            ref={textareaRef}
            rows={1}
            value={question}
            onChange={handleTextareaChange}
            placeholder="Ask a question about this document..."
            className="flex-1 resize-none overflow-y-auto card-bg rounded-2xl px-5 py-4 outline-none min-h-[56px] max-h-40 focus:ring-2 focus:ring-violet-500"
            onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                handleAsk();
                }
            }}
            />

            <button
            onClick={handleAsk}
            disabled={loading}
            className="h-14 w-14 rounded-2xl bg-violet-600 hover:bg-violet-700 hover:scale-105 active:scale-95 transition shadow-lg hover:shadow-violet-500/40 flex items-center justify-center disabled:opacity-50"
            >
            <FiSend size={22} />
            </button>

        </div>

    </div>
  </main>
</div>

  );
}

export default DocumentAI;