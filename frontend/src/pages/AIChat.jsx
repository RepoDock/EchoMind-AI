
import { chatWithAI } from "../services/api";
import Sidebar from "../components/Sidebar";
import Header from "../components/Header";
import { useState, useRef, useEffect } from "react";
import {
  ChevronDown,
  BookOpen,
  Brain,
  Trash2,
  Pencil,
} from "lucide-react";
function AIChat() {
  const messagesEndRef = useRef(null);
  const [mode, setMode] = useState("research");
  const [question, setQuestion] = useState("");
  const [showModes, setShowModes] = useState(false);
  const [messages, setMessages] = useState([]);
  const [isThinking, setIsThinking] = useState(false);
  const [chats, setChats] = useState([]);
  const [currentChatId, setCurrentChatId] = useState(null);
  const [showHistory, setShowHistory] = useState(false);
  const [editingChatId, setEditingChatId] = useState(null);
  const [editedTitle, setEditedTitle] = useState("");

useEffect(() => {
  const savedChats = localStorage.getItem("axon_chats");

  if (savedChats) {
    const parsed = JSON.parse(savedChats);
    setChats(parsed);
  }
}, []);

useEffect(() => {
  console.log("Chats State:", chats);

  if (chats.length > 0) {
    localStorage.setItem(
      "axon_chats",
      JSON.stringify(chats)
    );
  }

  console.log(
    "Saved:",
    localStorage.getItem("axon_chats")
  );
}, [chats]);
const newChat = () => {
  setMessages([]);
  setCurrentChatId(null);
  setQuestion("");
  setShowHistory(false);
};
const deleteChat = (chatId) => {
  const updatedChats = chats.filter((chat) => chat.id !== chatId);

  setChats(updatedChats);

  if (currentChatId === chatId) {
    setCurrentChatId(null);
    setMessages([]);
  }
};
const clearChatHistory = () => {

  const confirmClear = window.confirm(
    "Delete all chat history?"
  );

  if (!confirmClear) return;

  localStorage.removeItem("axon_chats");

  setChats([]);
  setMessages([]);
  setCurrentChatId(null);

};
const renameChat = (chatId) => {
  const updatedChats = chats.map((chat) =>
    chat.id === chatId
      ? {
          ...chat,
          title: editedTitle.trim() || chat.title,
        }
      : chat
  );

  setChats(updatedChats);

  setEditingChatId(null);
  setEditedTitle("");
};

const sendMessage = async () => {
  if (!question.trim()) return;

  const userQuestion = question;

  setQuestion("");
  setIsThinking(true);

  const userMessage = {
    role: "user",
    text: userQuestion,
  };

  const currentMessages = [...messages, userMessage];

  // User message turant UI me dikhao
  setMessages(currentMessages);

  try {
    const response = await chatWithAI(
      userQuestion,
      currentMessages,
      mode
    );
    console.log("AI Response:", response);

    const assistantMessage = {
      role: "assistant",
      text: response.data.answer,
      sources: response.data.sources,
    };

    const updatedMessages = [
      ...currentMessages,
      assistantMessage,
    ];

    setMessages(updatedMessages);
    console.log("Creating new chat...");
    console.log("Reached after AI response");
    if (currentChatId === null) {
      const chat = {
        id: Date.now(),
        title:
          userQuestion.length > 35
            ? userQuestion.slice(0, 35) + "..."
            : userQuestion,
        messages: updatedMessages,
      };
      console.log(chat);

      setChats((prev) => [chat, ...prev]);
      setCurrentChatId(chat.id);
    } else {
      setChats((prev) =>
        prev.map((chat) =>
          chat.id === currentChatId
            ? {
                ...chat,
                messages: updatedMessages,
              }
            : chat
        )
      );
    }
  } catch (error) {
    console.error(error);
  } finally {
    setIsThinking(false);
  }
};


  useEffect(() => {
  messagesEndRef.current?.scrollIntoView({
    behavior: "smooth",
  });
}, [messages, isThinking]);

  return (
    <div className="h-screen overflow-hidden app-bg flex">

    <Sidebar />

    <main className="flex-1 flex flex-col h-screen">

    {/* <Header /> */}
    <div className="relative flex flex-col h-full app-bg text-theme">


<div className="sticky top-0 z-50 flex justify-between items-center px-10 py-6 app-bg backdrop-blur-xl border-b border-theme">

    {messages.length > 0 ? (
        <h1 className="text-2xl font-semibold">
            AXON AI
        </h1>
    ) : (
        <div></div>
    )}

    <div className="flex gap-3">

        <button
            onClick={newChat}
            className="px-4 py-2 rounded-xl bg-cyan-500 hover:bg-cyan-400 transition"
        >
            + New Chat
        </button>

        <div className="relative">

            <button
              onClick={() => setShowHistory(!showHistory)}
              className="px-4 py-2 rounded-xl card-bg transition"
            >
              History
            </button>

            {showHistory && (

              <div className="absolute right-0 mt-2 w-80 card-bg rounded-xl shadow-2xl overflow-hidden z-50">

                {chats.length === 0 ? (

                  <div className="p-4 text-theme opacity-70 text-sm">
                    No chats yet
                  </div>

                ) : (

                  chats.map((chat) => (

                    <div
                      key={chat.id}
                      className="flex items-center justify-between border-b border-theme hover:opacity-80"
                    >

                      <button
                        onClick={() => {
                          setMessages(chat.messages);
                          setCurrentChatId(chat.id);
                          setShowHistory(false);
                        }}
                        className="flex-1 text-left px-4 py-3"
                      >
                       {editingChatId === chat.id ? (

                          <input
                            autoFocus
                            value={editedTitle}
                            onChange={(e) => setEditedTitle(e.target.value)}
                            onKeyDown={(e) => {
                              if (e.key === "Enter") {
                                renameChat(chat.id);
                              }
                            }}
                            className="bg-transparent outline-none text-theme w-full"
                          />

                        ) : (

                          <span>{chat.title}</span>

                        )}
                      </button>
                        <button
                        onClick={() => {
                          setEditingChatId(chat.id);
                          setEditedTitle(chat.title);
                        }}
                        className="px-2 text-cyan-400 hover:text-cyan-300"
                      >
                        <Pencil size={17} />
                      </button>
                      <button
                        onClick={() => deleteChat(chat.id)}
                        className="px-3 text-red-400 hover:text-red-500"
                      >
                        <Trash2 size={18} />
                      </button>

                    </div>

                  ))
                  

                )}

              </div>

            )}

          </div>

    </div>

</div>
      <div className="flex-1 overflow-y-auto px-10 pb-40 space-y-4">
        {messages.length === 0 && (

      <div className="flex flex-col items-center justify-center h-[65vh]">

          <div className="w-20 h-20 rounded-full bg-cyan-500/10 flex items-center justify-center mb-6">

              <Brain size={42} className="text-cyan-400"/>

          </div>

          <h1 className="text-5xl font-bold mb-3">

              AXON AI

          </h1>

          <p className="text-theme opacity-70 text-lg">

              Ask anything about your documents.

          </p>

          <p className="text-theme opacity-60 text-sm mt-2">

              Research mode is enabled by default.

          </p>

      </div>

      )}
     
        {messages.map((msg, index) => (

  <div
    key={index}
    className={
      msg.role === "user"
        ? "flex flex-col items-end"
        : "flex flex-col items-start"
    }
  >

   <div className="font-semibold text-cyan-400 mb-2">
      {msg.role === "user" ? "You" : "AXON"}
    </div>

    <div
      className={
        msg.role === "user"
          ? "bg-cyan-500/10 border border-cyan-500/20 rounded-2xl px-5 py-3 mt-2 max-w-xl"
          : "card-bg rounded-2xl px-5 py-3 mt-2 max-w-xl"
      }
    >

      {msg.text}

    </div>

    {msg.role === "assistant" &&
      msg.sources &&
      msg.sources.length > 0 && (

        <ul className="list-disc ml-6 mt-1">

            {msg.sources.map((source, index) => (

              <li key={index}>
                📄 {source.file}
              </li>

            ))}

          </ul>

    )}

  </div>

))}
        {isThinking && (

  <div className="flex flex-col items-start">

    <div className="font-semibold text-cyan-400">
      AXON
    </div>

    <div className="card-bg rounded-2xl p-5 mt-2 inline-flex items-center gap-2">

      <span className="w-2 h-2 bg-cyan-400 rounded-full animate-bounce"></span>

      <span
        className="w-2 h-2 bg-cyan-400 rounded-full animate-bounce"
        style={{ animationDelay: "0.2s" }}
      ></span>

      <span
        className="w-2 h-2 bg-cyan-400 rounded-full animate-bounce"
        style={{ animationDelay: "0.4s" }}
      ></span>

      <span className="ml-2 text-theme opacity-80">
        Thinking...
      </span>

    </div>

  </div>

)}
<div ref={messagesEndRef}></div>

      </div>
      <div className="sticky bottom-0 app-bg border-t border-theme p-6">

        <div className="relative">

          <input
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                sendMessage();
              }
            }}
            className="w-full card-bg rounded-full py-4 pl-6 pr-28 text-theme outline-none"
            placeholder={
              mode === "research"
                ? "Ask about your documents..."
                : "Ask anything..."
            }
          />

          <button
            onClick={sendMessage}
            className="absolute right-4 top-1/2 -translate-y-1/2 bg-cyan-500 hover:bg-cyan-400 rounded-full w-11 h-11 flex items-center justify-center"
          >
            ↑
          </button>
          

        </div>

        <div className="mt-3">

          <div className="relative inline-block">

            <button
              onClick={() => setShowModes(!showModes)}
              className="flex items-center gap-2 rounded-xl card-bg px-4 py-2 text-theme hover:opacity-80 transition"
            >

              {mode === "research" ? (
                <>
                  <BookOpen size={18} className="text-cyan-400" />
                  <span>Research</span>
                </>
              ) : (
                <>
                  <Brain size={18} className="text-green-400" />
                  <span>Learn</span>
                </>
              )}

              <ChevronDown size={16} />

            </button>

            {showModes && (

              <div className="absolute bottom-14 left-0 w-72 rounded-2xl card-bg shadow-2xl overflow-hidden">

                <button
                  onClick={() => {
                    setMode("research");
                    setShowModes(false);
                  }}
                  className="w-full text-left p-4 hover:bg-slate-800 transition"
                >
                  <div className="flex items-center gap-3">

                    <BookOpen className="text-cyan-400" size={20} />

                    <div>

                      <div className="font-semibold">
                        Research
                      </div>

                      <div className="text-xs text-theme opacity-70">
                        Docs Only
                      </div>

                    </div>

                  </div>
                </button>

                <button
                  onClick={() => {
                    setMode("learn");
                    setShowModes(false);
                  }}
                  className="w-full text-left p-4 hover:bg-slate-800 transition"
                >
                  <div className="flex items-center gap-3">

                    <Brain className="text-green-400" size={20} />

                    <div>

                      <div className="font-semibold">
                        Learn
                      </div>

                      <div className="text-xs text-theme opacity-70">
                        Docs + AI
                      </div>

                    </div>

                  </div>

                </button>

              </div>

            )}

          </div>

        </div>

      </div>



    </div>
    </main>

</div>

  );

}

export default AIChat;