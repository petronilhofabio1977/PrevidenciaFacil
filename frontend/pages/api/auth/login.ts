import type { NextApiRequest, NextApiResponse } from 'next';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  const { username, password } = req.body;
  
  const response = await fetch('http://previdencia_backend:8000/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({ username, password }).toString(),
  });
  
  const data = await response.json();
  res.status(response.status).json(data);
}
