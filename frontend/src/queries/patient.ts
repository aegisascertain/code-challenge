import { useQuery } from '@tanstack/react-query';
import { apiRequest } from './api';
import { components, operations } from './schema';

// Export schema types for use in components
export type Patient = components['schemas']['Patient'];
export type PatientResponse = components['schemas']['PatientResponse'];
export type PatientSearchParams =
  operations['search_patients_patients__get']['parameters']['query'];
export type PatientDetailsResponse = components['schemas']['PatientDetailsResponse'];

// Constants
const PATIENTS_ENDPOINT = '/patients/';

// Keys for React Query
export const patientKeys = {
  all: ['patients'] as const,
  list: () => [...patientKeys.all, 'list'] as const,
  search: (params: PatientSearchParams) => [...patientKeys.list(), params] as const,
  detail: (id: string) => [...patientKeys.all, 'detail', id] as const,
};

/**
 * Fetch patients from the API
 */
export const fetchPatients = async (params?: PatientSearchParams): Promise<PatientResponse> => {
  const searchParams = new URLSearchParams();

  if (params?.name) {
    searchParams.append('name', params.name);
  }

  if (params?.birthDate) {
    searchParams.append('birthDate', params.birthDate);
  }

  if (params?.threshold) {
    searchParams.append('threshold', params.threshold.toString());
  }

  const queryString = searchParams.toString();
  const url = `${PATIENTS_ENDPOINT}${queryString ? `?${queryString}` : ''}`;

  return apiRequest<PatientResponse>(url);
};

/**
 * Fetch a single patient's details
 */
export const fetchPatientDetails = async (patientId: string): Promise<PatientDetailsResponse> => {
  return apiRequest<PatientDetailsResponse>(`${PATIENTS_ENDPOINT}${patientId}`);
};

/**
 * Hook to get patients with optional search parameters
 */
export const usePatients = (params?: PatientSearchParams) => {
  return useQuery({
    queryKey: patientKeys.search(params || {}),
    queryFn: () => fetchPatients(params),
  });
};

/**
 * Hook to get a single patient's details
 */
export const usePatientDetails = (patientId: string) => {
  return useQuery({
    queryKey: patientKeys.detail(patientId),
    queryFn: () => fetchPatientDetails(patientId),
    enabled: !!patientId,
  });
};
