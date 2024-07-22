import React, { useState } from 'react';
import useAuth from '../../hooks/useAuth';
import { PredictionService } from '../../client';
import { InputData, Message } from '../../client';

const Prediction = () => {
    const { user } = useAuth();
    const [modelName, setModelName] = useState('');
    const [inputData, setInputData] = useState<string>('');
    const [result, setResult] = useState<Message | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState(false);

    const handlePrediction = async () => {
        if (!modelName) {
            setError('Please select a model.');
            return;
        }

        if (!inputData) {
            setError('Please enter input data.');
            return;
        }

        setIsLoading(true);
        setError(null);
        setResult(null);

        try {
            const parsedInputData: InputData = JSON.parse(inputData);
            const response = await PredictionService.makePrediction({
                modelName,
                inputData: parsedInputData
            });
            
            setResult(response);
        } catch (error: any) {
            if (error instanceof SyntaxError) {
                setError('Invalid JSON input. Please check your input data.');
            } else {
                setError(`Prediction failed: ${error.message}`);
            }
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div>
            <h2>Make a Prediction</h2>
            <p>Current user: {user?.email}</p>
            <select 
                value={modelName} 
                onChange={(e) => setModelName(e.target.value)}
                disabled={isLoading}
            >
                <option value="">Select a model</option>
                <option value="model1">Model 1</option>
                <option value="model2">Model 2</option>
                <option value="model3">Model 3</option>
            </select>
            <textarea
                value={inputData}
                onChange={(e) => setInputData(e.target.value)}
                placeholder="Enter input data as JSON"
                disabled={isLoading}
            />
            <button onClick={handlePrediction} disabled={isLoading || !modelName || !inputData}>
                {isLoading ? 'Processing...' : 'Predict'}
            </button>
            {error && <p style={{color: 'red'}}>{error}</p>}
            {result && (
                <div>
                    <h3>Prediction Result:</h3>
                    <p>{result.message}</p>
                    <p>Credits added: {result.credits_added}</p>
                </div>
            )}
        </div>
    );
};

export default Prediction;
