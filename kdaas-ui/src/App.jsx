import { useState } from "react";
import { Card, CardContent } from "./components/ui/card";
import { Button } from "./components/ui/button";
import { Input } from "./components/ui/input";
import { Textarea } from "./components/ui/textarea";
import { Progress } from "./components/ui/progress";

export default function App() {
  const [teacherModel, setTeacherModel] = useState(null);
  const [dataset, setDataset] = useState(null);
  const [prompt, setPrompt] = useState("");
  const [progress, setProgress] = useState(0);
  const [training, setTraining] = useState(false);
  const [chatMessages, setChatMessages] = useState([
    { role: "bot", content: "Hey there! I'm here to help you with model miniaturization. Tell me what you're aiming to achieve, and we can figure it out together!" }
  ]);
  const [chatInput, setChatInput] = useState("");
  const [finalRequirements, setFinalRequirements] = useState(null);

  const handleUpload = (event, type) => {
    const file = event.target.files[0];
    if (type === "teacher") setTeacherModel(file);
    if (type === "dataset") setDataset(file);
  };

  const handleChatSend = () => {
    if (!chatInput.trim()) return;
    setChatMessages([...chatMessages, { role: "user", content: chatInput }]);
    setChatInput("");
    
    // Simulating bot response
    setTimeout(() => {
      const botResponse = `I understand you want to distill knowledge from the teacher model using the dataset. Can you confirm these details?`;
      setChatMessages((prevMessages) => [...prevMessages, { role: "bot", content: botResponse }]);
    }, 1000);
  };

  const handleConfirmRequirements = () => {
    const formattedRequirements = chatMessages.filter(m => m.role === "user").map(m => m.content).join(" ");
    setFinalRequirements(formattedRequirements);
  };

  const handleTrain = () => {
    if (!teacherModel || !dataset || !finalRequirements) {
      alert("Please complete all steps, confirm requirements, and upload necessary files.");
      return;
    }
    setTraining(true);
    setProgress(10);

    // Simulating training process
    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval);
          setTraining(false);
          return 100;
        }
        return prev + 10;
      });
    }, 1000);
  };

  return (
    <div className="flex justify-center items-center min-h-screen w-screen bg-gray-900 p-4">
      <div className="max-w-6xl w-full p-8 bg-gray-800 shadow-lg rounded-lg flex gap-6">
        {/* File Upload Section (Left) */}
        <Card className="p-6 bg-gray-700 rounded-lg flex-1">
          <CardContent className="space-y-6">
            <h2 className="text-xl font-bold text-white">Upload Files</h2>
            <div>
              <label className="block text-sm font-medium mb-2 text-white">Upload Teacher Model</label>
              <Input type="file" accept=".pt,.h5" className="bg-gray-600 text-white w-full" onChange={(e) => handleUpload(e, "teacher")} />
            </div>
            <div>
              <label className="block text-sm font-medium mb-2 text-white">Upload Dataset</label>
              <Input type="file" accept=".csv,.json" className="bg-gray-600 text-white w-full" onChange={(e) => handleUpload(e, "dataset")} />
            </div>
            <Button className="bg-orange-500 hover:bg-orange-600 text-white w-full py-3 text-lg rounded-lg mt-6 mb-6" onClick={handleTrain} disabled={training}>
              {training ? "Training in Progress..." : "Start Distillation"}
            </Button>
            {training && <Progress value={progress} className="mt-4 w-full" />}
          </CardContent>
        </Card>

        {/* Chatbot Section (Right) */}
        <Card className="p-6 bg-gray-700 rounded-lg flex-1 h-full">
          <CardContent className="flex flex-col h-full space-y-4">
            <h2 className="text-xl font-bold text-white">Chat with Assistant</h2>
            <div className="flex-1 h-[400px] w-full overflow-y-auto bg-gray-800 p-3 rounded-md text-white">
              {chatMessages.map((msg, index) => (
                <div key={index} className={msg.role === "user" ? "text-right" : "text-left"}>
                  <p className="p-2 bg-gray-800 rounded-md inline-block">{msg.content}</p>
                </div>
              ))}
            </div>
            <div className="flex gap-2 mt-4 w-full">
              <Input value={chatInput} onChange={(e) => setChatInput(e.target.value)} placeholder="Describe your requirements..." className="flex-1" />
              <Button onClick={handleChatSend} className="w-24 bg-blue-500 hover:bg-blue-600 text-white">Send</Button>
            </div>
            {chatMessages.length > 0 && (
              <Button onClick={handleConfirmRequirements} className="bg-green-500 hover:bg-green-600 text-white w-full">Confirm Requirements</Button>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
