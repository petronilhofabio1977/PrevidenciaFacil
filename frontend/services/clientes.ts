import api from './api';

export interface Cliente {
  id: string;
  nome_completo: string;
  cpf: string;
  data_nascimento: string;
  sexo: string;
  categoria_segurado: string;
  data_filiacao_rgps?: string;
  professor: boolean;
  atividade_rural: boolean;
  deficiencia: string;
  criado_em: string;
}

export interface ClienteInput {
  nome_completo: string;
  cpf: string;
  data_nascimento: string;
  sexo: string;
  categoria_segurado: string;
  data_filiacao_rgps?: string;
  professor: boolean;
  atividade_rural: boolean;
  deficiencia: string;
}

export const clientesAPI = {
  listar: async (): Promise<Cliente[]> => {
    const response = await api.get('/clientes/');
    return response.data;
  },

  criar: async (data: ClienteInput): Promise<Cliente> => {
    const response = await api.post('/clientes/', data);
    return response.data;
  },

  obter: async (id: string): Promise<Cliente> => {
    const response = await api.get(`/clientes/${id}`);
    return response.data;
  },

  atualizar: async (id: string, data: ClienteInput): Promise<Cliente> => {
    const response = await api.put(`/clientes/${id}`, data);
    return response.data;
  },

  deletar: async (id: string): Promise<void> => {
    await api.delete(`/clientes/${id}`);
  }
};
