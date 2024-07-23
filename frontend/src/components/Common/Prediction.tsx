import { useState } from 'react';
import useAuth from '../../hooks/useAuth';
import { PredictionService } from '../../client';
import { InputData, Message2 } from '../../client';

const Prediction = () => {
    const { user } = useAuth();
    const [modelName, setModelName] = useState('');
    const [inputData, setInputData] = useState<InputData>({
        married: 0,
        income: 0,
        education: 0,
        loan_amount: 0,
        credit_history: 0,
    });
    const [result, setResult] = useState<Message2 | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState(false);

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        setInputData(prev => ({
            ...prev,
            [name]: parseFloat(value),
        }));
    };

    const handlePrediction = async () => {
        if (!modelName) {
            setError('Please select a model.');
            return;
        }

        setIsLoading(true);
        setError(null);
        setResult(null);

        try {
            const response = await PredictionService.makePrediction({
                modelName,
                inputData,
            });

            // Assume the response has prediction and credits_left properties
            const { prediction, credits_left } = response;
            setResult({ prediction, credits_left });
        } catch (error: any) {
            setError(`Prediction failed: ${error.message}`);
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

            <div>
                <label>
                    Married:
                    <input
                        type="number"
                        name="married"
                        value={inputData.married}
                        onChange={handleInputChange}
                        disabled={isLoading}
                    />
                </label>
            </div>

            <div>
                <label>
                    Income:
                    <input
                        type="number"
                        name="income"
                        value={inputData.income}
                        onChange={handleInputChange}
                        disabled={isLoading}
                    />
                </label>
            </div>

            <div>
                <label>
                    Education:
                    <input
                        type="number"
                        name="education"
                        value={inputData.education}
                        onChange={handleInputChange}
                        disabled={isLoading}
                    />
                </label>
            </div>

            <div>
                <label>
                    Loan Amount:
                    <input
                        type="number"
                        name="loan_amount"
                        value={inputData.loan_amount}
                        onChange={handleInputChange}
                        disabled={isLoading}
                    />
                </label>
            </div>

            <div>
                <label>
                    Credit History:
                    <input
                        type="number"
                        name="credit_history"
                        value={inputData.credit_history}
                        onChange={handleInputChange}
                        disabled={isLoading}
                    />
                </label>
            </div>

            <button onClick={handlePrediction} disabled={isLoading || !modelName}>
                {isLoading ? 'Processing...' : 'Predict'}
            </button>

            {error && <p style={{ color: 'red' }}>{error}</p>}
            {result && (
                <div>
                    <h3>Prediction Result:</h3>
                    <p>Prediction: {result.prediction}</p>
                    <p>Credits Left: {result.credits_left}</p>
                </div>
            )}
        </div>
    );
};

export default Prediction;
