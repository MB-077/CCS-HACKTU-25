export interface Idata {
  first_name?: string;
  last_name?: string;
  email?: string;
  phone_number?: number;
  password?: string;
  confirm_password?: string;
}

export interface IData {
  username: string;
  password: string;
}

export interface ApiResponse {
  data: {
    token: string;
  };
}
