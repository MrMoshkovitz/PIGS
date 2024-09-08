import React, { useState } from 'react';
import { Button } from "./components/ui/button"
import { Textarea } from "./components/ui/textarea"
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from "./components/ui/card"
import { Loader2, Zap } from "lucide-react"

const App = () => {
  const [prompt, setPrompt] = useState('');
  const [result, setResult] = useState('');
  const [analysis, setAnalysis] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');
    setResult('');
    setAnalysis('');

    try {
      const response = await fetch('http://localhost:8000/optimize_prompt', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt: prompt })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'An error occurred while processing your request.');
      }

      const data = await response.json();
      setResult(data.improved_prompt);
      setAnalysis(data.analysis);
    } catch (error) {
      console.error('Error:', error);
      setError(error.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-600 to-blue-500 flex items-center justify-center p-4">
      <Card className="w-full max-w-2xl shadow-2xl bg-white bg-opacity-95 backdrop-blur-sm">
        <CardHeader className="bg-gradient-to-r from-purple-600 to-blue-500 text-white rounded-t-lg">
          <CardTitle className="text-3xl font-bold text-center flex items-center justify-center">
            <Zap className="mr-2" /> PromptPro AI
          </CardTitle>
          <CardDescription className="text-center text-gray-100">
            Enhance your prompts with advanced AI techniques
          </CardDescription>
        </CardHeader>
        <CardContent className="mt-6">
          <form onSubmit={handleSubmit} className="space-y-6">
            <Textarea
              placeholder="Enter your prompt here (you can write multiple lines)"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              className="w-full p-3 border border-gray-300 rounded-lg min-h-[150px] focus:ring-2 focus:ring-purple-500 focus:border-transparent"
            />
            <Button 
              type="submit" 
              className="w-full bg-gradient-to-r from-purple-600 to-blue-500 hover:from-purple-700 hover:to-blue-600 text-white font-semibold py-3 rounded-lg transition duration-300 transform hover:scale-105" 
              disabled={isLoading || !prompt.trim()}
            >
              {isLoading ? (
                <>
                  <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                  Optimizing...
                </>
              ) : (
                <>
                  <Zap className="mr-2 h-5 w-5" />
                  Optimize Prompt
                </>
              )}
            </Button>
          </form>
        </CardContent>
        <CardFooter className="flex flex-col space-y-4">
          {error && (
            <div className="w-full p-4 bg-red-100 border-l-4 border-red-500 text-red-700 rounded-r-lg">
              <p className="font-medium">Error:</p>
              <p className="mt-1">{error}</p>
            </div>
          )}
          {result && (
            <div className="w-full p-4 bg-green-50 border-l-4 border-green-500 rounded-r-lg">
              <p className="font-medium text-green-800">Improved Prompt:</p>
              <p className="mt-2 text-green-700 whitespace-pre-wrap">{result}</p>
            </div>
          )}
          {analysis && (
            <div className="w-full p-4 bg-blue-50 border-l-4 border-blue-500 rounded-r-lg">
              <p className="font-medium text-blue-800">Analysis:</p>
              <p className="mt-2 text-blue-700 whitespace-pre-wrap">{analysis}</p>
            </div>
          )}
        </CardFooter>
      </Card>
    </div>
  );
};

export default App;