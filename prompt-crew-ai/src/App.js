import React, { useState } from 'react';
import { Button } from "./components/ui/button"
import { Textarea } from "./components/ui/textarea"
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from "./components/ui/card"
import { Loader2, FileSpreadsheet } from "lucide-react"

const App = () => {
  const [request, setRequest] = useState('');
  const [result, setResult] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');
    setResult('');

    try {
      const response = await fetch('http://localhost:8000/create_spreadsheet', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ request: request })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error?.message || 'An error occurred while processing your request.');
      }

      const data = await response.json();
      setResult(data.result);
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
            <FileSpreadsheet className="mr-2" /> Excel Specialist AI
          </CardTitle>
          <CardDescription className="text-center text-gray-100">
            Create custom spreadsheets for commercial cleaning job costing
          </CardDescription>
        </CardHeader>
        <CardContent className="mt-6">
          <form onSubmit={handleSubmit} className="space-y-6">
            <Textarea
              placeholder="Describe your spreadsheet requirements here..."
              value={request}
              onChange={(e) => setRequest(e.target.value)}
              className="w-full p-3 border border-gray-300 rounded-lg min-h-[150px] focus:ring-2 focus:ring-purple-500 focus:border-transparent"
            />
            <Button 
              type="submit" 
              className="w-full bg-gradient-to-r from-purple-600 to-blue-500 hover:from-purple-700 hover:to-blue-600 text-white font-semibold py-3 rounded-lg transition duration-300 transform hover:scale-105" 
              disabled={isLoading || !request.trim()}
            >
              {isLoading ? (
                <>
                  <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                  Creating Spreadsheet...
                </>
              ) : (
                <>
                  <FileSpreadsheet className="mr-2 h-5 w-5" />
                  Create Spreadsheet
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
              <p className="font-medium text-green-800">Spreadsheet Creation Result:</p>
              <p className="mt-2 text-green-700 whitespace-pre-wrap">{result}</p>
            </div>
          )}
        </CardFooter>
      </Card>
    </div>
  );
};

export default App;