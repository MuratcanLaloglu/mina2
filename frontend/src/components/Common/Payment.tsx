import { useState } from 'react';
import useAuth from '../../hooks/useAuth';
import { PaymentService } from '../../client';
import { Button, Select } from '@chakra-ui/react';

const Payment = () => {
    const { user } = useAuth();
    const [option, setOption] = useState('');
    const [message, setMessage] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const handlePayment = async () => {
        if (!option) {
            setMessage('Please select a payment option.');
            return;
        }

        setIsLoading(true);
        setMessage('');

        try {
            const response = await PaymentService.makePayment({option});
            setMessage(`Payment successful! Credits added: ${response.credits_added}`);
        } catch (error: any) {
            setMessage(`Payment failed: ${error.message}`);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div>
            <h2>Make a Payment</h2>
            <p>Current user: {user?.email}</p>
            <Select value={option} onChange={(e) => setOption(e.target.value)}>
                <option value="">Select an option</option>
                <option value="model1">Model 1 ($30)</option>
                <option value="model2">Model 2 ($60)</option>
                <option value="model3">Model 3 ($90)</option>
                <option value="all">All Models ($100)</option>
            </Select>
            <Button onClick={handlePayment} disabled={!option || isLoading}>
                {isLoading ? 'Processing...' : 'Pay'}
            </Button>
            {message && <p>{message}</p>}
        </div>
    );
};

export default Payment;
