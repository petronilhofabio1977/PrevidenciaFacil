import { useState, useEffect } from 'react';
import { documentosAPI, Documento, DashboardValidacao } from '../services/documentos';

export function useDocumentos(clienteId?: string) {
  const [documentos, setDocumentos] = useState<Documento[]>([]);
  const [dashboard, setDashboard] = useState<DashboardValidacao | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const carregarDocumentos = async (id: string) => {
    setLoading(true);
    try {
      const data = await documentosAPI.listarPorCliente(id);
      setDocumentos(data);
      setError(null);
    } catch (err) {
      setError('Erro ao carregar documentos');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const carregarDashboard = async () => {
    setLoading(true);
    try {
      const data = await documentosAPI.getDashboard();
      setDashboard(data);
      setError(null);
    } catch (err) {
      setError('Erro ao carregar dashboard');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const uploadDocumento = async (id: string, tipo: string, file: File) => {
    setLoading(true);
    try {
      const result = await documentosAPI.upload(id, tipo, file);
      await carregarDocumentos(id);
      await carregarDashboard();
      return result;
    } catch (err) {
      setError('Erro no upload');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    carregarDashboard();
  }, []);

  useEffect(() => {
    if (clienteId) {
      carregarDocumentos(clienteId);
    }
  }, [clienteId]);

  return {
    documentos,
    dashboard,
    loading,
    error,
    uploadDocumento,
    refresh: () => {
      if (clienteId) carregarDocumentos(clienteId);
      carregarDashboard();
    }
  };
}
