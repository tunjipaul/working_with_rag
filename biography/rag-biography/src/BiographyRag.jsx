import React, { useState, useRef, useEffect } from "react";
import {
  Upload,
  Send,
  Trash2,
  Key,
  User,
  Bot,
  Loader2,
  AlertCircle,
  TrendingUp,
} from "lucide-react";

export default function BiographyRAG() {
  const [apiKey, setApiKey] = useState("");
  const [file, setFile] = useState(null);
  const [sessionId, setSessionId] = useState("");
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [usage, setUsage] = useState(null);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);
  const fileInputRef = useRef(null);

  const API_URL = "http://localhost:8000";

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    if (apiKey && sessionId) {
      fetchUsage();
      const interval = setInterval(fetchUsage, 30000); // Update every 30 seconds
      return () => clearInterval(interval);
    }
  }, [apiKey, sessionId]);

  const fetchUsage = async () => {
    if (!apiKey) return;

    try {
      const response = await fetch(`${API_URL}/usage/${apiKey}`);
      if (response.ok) {
        const data = await response.json();
        setUsage(data);
      }
    } catch (err) {
      console.error("Failed to fetch usage:", err);
    }
  };

  const handleError = (error, defaultMsg) => {
    let errorMessage = defaultMsg;
    let waitTime = null;

    if (error.detail) {
      if (typeof error.detail === "object") {
        errorMessage = error.detail.message || defaultMsg;
        waitTime = error.detail.wait_time;
        if (error.detail.usage) {
          setUsage(error.detail.usage);
        }
      } else {
        errorMessage = error.detail;
      }
    }

    if (waitTime) {
      errorMessage += ` Please wait ${Math.ceil(waitTime)} seconds.`;
    }

    setError(errorMessage);
    setTimeout(() => setError(null), 8000);
  };

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && selectedFile.name.endsWith(".txt")) {
      setFile(selectedFile);
      setError(null);
    } else {
      setError("Please select a .txt file");
      setTimeout(() => setError(null), 3000);
    }
  };

  const handleUpload = async () => {
    console.log("Upload started");

    if (!apiKey) {
      console.log("No API key provided");
      setError("Please enter your Google API key");
      setTimeout(() => setError(null), 3000);
      return;
    }
    if (!file) {
      console.log("No file selected");
      setError("Please select a file");
      setTimeout(() => setError(null), 3000);
      return;
    }

    setUploading(true);
    setError(null);
    const formData = new FormData();
    formData.append("file", file);

    console.log("FormData created with file:", file.name);
    console.log(
      "API URL:",
      `${API_URL}/upload?api_key=${apiKey.substring(0, 10)}...`
    );

    try {
      console.log("Sending upload request...");
      const response = await fetch(`${API_URL}/upload?api_key=${apiKey}`, {
        method: "POST",
        body: formData,
      });

      console.log("Response status:", response.status);
      const data = await response.json();
      console.log("Response data:", data);

      if (!response.ok) {
        console.error(
          "Upload failed with status:",
          response.status,
          "Data:",
          data
        );
        handleError(data, "Upload failed");
        return;
      }

      console.log("Upload successful! Session ID:", data.session_id);
      setSessionId(data.session_id);
      setMessages([]);
      setUsage(data.usage);
      setError(null);
    } catch (error) {
      console.error("Network error during upload:", error);
      setError(`Network error: ${error.message}`);
      setTimeout(() => setError(null), 5000);
    } finally {
      setUploading(false);
    }
  };

  const handleSendMessage = async () => {
    console.log("Send message started");
    console.log("Input:", input);
    console.log("Session ID:", sessionId);

    if (!input.trim() || !sessionId) {
      console.log("Cannot send: input empty or no session");
      return;
    }

    const userMessage = { role: "user", content: input };
    setMessages((prev) => [...prev, userMessage]);
    const currentInput = input;
    setInput("");
    setLoading(true);
    setError(null);

    console.log("Sending query:", currentInput);

    try {
      const payload = {
        session_id: sessionId,
        question: currentInput,
        api_key: apiKey,
      };
      console.log("Request payload:", payload);

      const response = await fetch(`${API_URL}/query`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      console.log("Response status:", response.status);
      const data = await response.json();
      console.log("Full Response data:", JSON.stringify(data, null, 2));

      if (response.status === 429) {
        const waitTime = data.detail?.wait_time || 10;
        console.warn("Rate limited. Wait time:", waitTime);
        setError(
          `Rate limit hit. Please wait ${Math.ceil(
            waitTime
          )} seconds before trying again.`
        );
        setMessages((prev) => prev.slice(0, -1));
        setLoading(false);
        return;
      }

      if (!response.ok) {
        console.error("Query failed:", data);
        handleError(data, "Query failed");
        setMessages((prev) => prev.slice(0, -1));
        return;
      }

      console.log("Query successful! Answer:", data.answer);
      const assistantMessage = { role: "assistant", content: data.answer };
      setMessages((prev) => [...prev, assistantMessage]);
      setUsage(data.usage);
    } catch (error) {
      console.error("Network error during query:", error);
      setError(`Network error: ${error.message}`);
      setMessages((prev) => prev.slice(0, -1));
    } finally {
      setLoading(false);
    }
  };
  const handleClearChat = () => {
    if (window.confirm("Clear chat history?")) {
      setMessages([]);
    }
  };

  const handleReset = () => {
    if (
      window.confirm(
        "Reset everything? This will clear the biography and chat history."
      )
    ) {
      setSessionId("");
      setMessages([]);
      setFile(null);
      setUsage(null);
      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }
    }
  };

  const UsageBar = ({ used, limit, label, color }) => {
    const percentage = (used / limit) * 100;
    const isWarning = percentage > 70;
    const isDanger = percentage > 90;

    return (
      <div className="mb-3">
        <div className="flex justify-between text-xs mb-1">
          <span className="text-gray-600">{label}</span>
          <span
            className={`font-medium ${
              isDanger
                ? "text-red-600"
                : isWarning
                ? "text-orange-600"
                : "text-gray-700"
            }`}
          >
            {used} / {limit}
          </span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div
            className={`h-2 rounded-full transition-all duration-300 ${
              isDanger ? "bg-red-500" : isWarning ? "bg-orange-500" : color
            }`}
            style={{ width: `${Math.min(percentage, 100)}%` }}
          />
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-linear-to-br from-blue-50 to-indigo-100 p-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-6 pt-6">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">
            👤 Interactive Biography
          </h1>
          <p className="text-gray-600">
            Upload a biography and chat with it using AI
          </p>
        </div>

        {/* Error Alert */}
        {error && (
          <div className="mb-4 bg-red-50 border border-red-200 rounded-lg p-4 flex items-start">
            <AlertCircle className="w-5 h-5 text-red-600 mr-3 shrink-0 mt-0.5" />
            <div className="flex-1">
              <h3 className="text-red-800 font-medium">Error</h3>
              <p className="text-red-700 text-sm mt-1">{error}</p>
            </div>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Sidebar */}
          <div className="lg:col-span-1 space-y-4">
            {/* API Key */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="flex items-center mb-4">
                <Key className="w-5 h-5 text-indigo-600 mr-2" />
                <h2 className="text-lg font-semibold text-gray-800">API Key</h2>
              </div>
              <input
                type="password"
                placeholder="Google API Key"
                value={apiKey}
                onChange={(e) => setApiKey(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none"
              />
              <a
                href="https://aistudio.google.com/app/apikey"
                target="_blank"
                rel="noopener noreferrer"
                className="text-sm text-indigo-600 hover:underline mt-2 inline-block"
              >
                Get Free API Key →
              </a>
            </div>

            {/* File Upload */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="flex items-center mb-4">
                <Upload className="w-5 h-5 text-indigo-600 mr-2" />
                <h2 className="text-lg font-semibold text-gray-800">
                  Upload Biography
                </h2>
              </div>
              <input
                ref={fileInputRef}
                type="file"
                accept=".txt"
                onChange={handleFileChange}
                className="w-full text-sm text-gray-600 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100 cursor-pointer"
              />
              {file && (
                <div className="mt-3 p-2 bg-green-50 rounded text-sm text-green-700 flex items-center">
                  <span className="mr-2">✓</span>
                  <span className="truncate">{file.name}</span>
                </div>
              )}
              <button
                onClick={handleUpload}
                disabled={!apiKey || !file || uploading}
                className="w-full mt-4 bg-indigo-600 text-white py-2 px-4 rounded-lg hover:bg-indigo-700 disabled:bg-gray-300 disabled:cursor-not-allowed flex items-center justify-center font-medium transition"
              >
                {uploading ? (
                  <>
                    <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                    Processing...
                  </>
                ) : (
                  <>
                    <Upload className="w-4 h-4 mr-2" />
                    Process Biography
                  </>
                )}
              </button>
            </div>

            {/* Usage Statistics */}
            {usage && (
              <div className="bg-white rounded-lg shadow-md p-6">
                <div className="flex items-center mb-4">
                  <TrendingUp className="w-5 h-5 text-indigo-600 mr-2" />
                  <h2 className="text-lg font-semibold text-gray-800">
                    API Usage
                  </h2>
                </div>
                <UsageBar
                  used={usage.rpm_used}
                  limit={usage.rpm_limit}
                  label="Requests per Minute"
                  color="bg-blue-500"
                />
                <UsageBar
                  used={usage.rpd_used}
                  limit={usage.rpd_limit}
                  label="Requests per Day"
                  color="bg-indigo-500"
                />
                <div className="text-xs text-gray-500 mt-2">
                  Free tier limits: {usage.rpm_limit} RPM, {usage.rpd_limit} RPD
                </div>
              </div>
            )}

            {/* Actions */}
            {sessionId && (
              <div className="bg-white rounded-lg shadow-md p-6 space-y-3">
                <h2 className="text-lg font-semibold text-gray-800 mb-4">
                  Actions
                </h2>
                <button
                  onClick={handleClearChat}
                  className="w-full bg-orange-500 text-white py-2 px-4 rounded-lg hover:bg-orange-600 flex items-center justify-center font-medium transition"
                >
                  <Trash2 className="w-4 h-4 mr-2" />
                  Clear Chat
                </button>
                <button
                  onClick={handleReset}
                  className="w-full bg-red-500 text-white py-2 px-4 rounded-lg hover:bg-red-600 flex items-center justify-center font-medium transition"
                >
                  <Trash2 className="w-4 h-4 mr-2" />
                  Reset All
                </button>
              </div>
            )}
          </div>

          {/* Chat Area */}
          <div className="lg:col-span-2 bg-white rounded-lg shadow-md flex flex-col h-150">
            {/* Chat Header */}
            <div className="bg-indigo-600 text-white p-4 rounded-t-lg">
              <h2 className="text-xl font-semibold">Chat</h2>
              {sessionId && usage && (
                <p className="text-sm text-indigo-100">
                  Active • {usage.rpd_remaining} requests remaining today
                </p>
              )}
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-6 space-y-4">
              {!sessionId ? (
                <div className="text-center text-gray-500 mt-20">
                  <Upload className="w-16 h-16 mx-auto mb-4 text-gray-300" />
                  <p className="text-lg font-medium">
                    Upload a biography to start chatting
                  </p>
                  <p className="text-sm mt-2">
                    Enter your API key and upload a .txt file
                  </p>
                </div>
              ) : messages.length === 0 ? (
                <div className="text-center text-gray-500 mt-20">
                  <Bot className="w-16 h-16 mx-auto mb-4 text-gray-300" />
                  <p className="text-lg font-medium">
                    Ready to answer your questions!
                  </p>
                  <p className="text-sm mt-2">
                    Try asking about their life, achievements, or experiences
                  </p>
                </div>
              ) : (
                messages.map((msg, idx) => (
                  <div
                    key={idx}
                    className={`flex ${
                      msg.role === "user" ? "justify-end" : "justify-start"
                    }`}
                  >
                    <div
                      className={`flex items-start max-w-[80%] ${
                        msg.role === "user" ? "flex-row-reverse" : "flex-row"
                      }`}
                    >
                      <div
                        className={`shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
                          msg.role === "user"
                            ? "bg-indigo-600 ml-3"
                            : "bg-gray-200 mr-3"
                        }`}
                      >
                        {msg.role === "user" ? (
                          <User className="w-5 h-5 text-white" />
                        ) : (
                          <Bot className="w-5 h-5 text-gray-600" />
                        )}
                      </div>
                      <div
                        className={`px-4 py-2 rounded-lg ${
                          msg.role === "user"
                            ? "bg-indigo-600 text-white"
                            : "bg-gray-100 text-gray-800"
                        }`}
                      >
                        <p className="text-sm whitespace-pre-wrap">
                          {msg.content}
                        </p>
                      </div>
                    </div>
                  </div>
                ))
              )}
              {loading && (
                <div className="flex justify-start">
                  <div className="flex items-center bg-gray-100 px-4 py-2 rounded-lg">
                    <Loader2 className="w-4 h-4 text-gray-600 animate-spin mr-2" />
                    <span className="text-sm text-gray-600">Thinking...</span>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>

            {/* Input */}
            <div className="border-t p-4">
              <div className="flex gap-2">
                <input
                  type="text"
                  placeholder={
                    sessionId
                      ? "Ask me anything about my life..."
                      : "Upload a biography first"
                  }
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyPress={(e) => e.key === "Enter" && handleSendMessage()}
                  disabled={!sessionId || loading}
                  className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none disabled:bg-gray-100 disabled:cursor-not-allowed"
                />
                <button
                  onClick={handleSendMessage}
                  disabled={!sessionId || !input.trim() || loading}
                  className="bg-indigo-600 text-white p-2 rounded-lg hover:bg-indigo-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition"
                >
                  <Send className="w-5 h-5" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
