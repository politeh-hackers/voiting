import { getToken } from "../utils/auth";

export interface BaseUUIDSchema {
    id?: string,
}

export interface Error {
    error: string
}

export class ApiService<T> {
    baseUrl: string = "http://localhost:8000"
    

    public async getAll(prefix: string): Promise<T[]> {
        const token = getToken()
        console.log("ddsds",token)
        const response = await fetch(`${this.baseUrl}/${prefix}/`,{
            headers:{
                'Authorization': `${token}`
            }
        });
        const jsonData = await response.json()
        return jsonData as T[]
    }

    public async create(data: T, prefix: string): Promise<void | Error> {
        
        const response = await fetch(`${this.baseUrl}/${prefix}/`, {
            method: 'POST',
            headers: {
                'Authorization': `${token}`,
                'Content-Type': 'application/json', // Указание типа контента
            },

            body: JSON.stringify(data)
        });
        if (response.status !== 200) {
            return await response.json() as Error
        }
        return response.json() ;
    }
    public async delete(prefix: string,id: string):Promise<void>{
        const response = await fetch(`${this.baseUrl}/${prefix}/${id}`,{
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json', // Указание типа контента
            },
            
        });
    }
    public async patch(prefix: string,id: string, data:T):Promise<void>{
        const response = await fetch(`${this.baseUrl}/${prefix}/${id}`,{
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json', // Указание типа контента
            },
            body: JSON.stringify(data)
        })
    }
}

export interface Post extends BaseUUIDSchema {
    name: string
}

export class PostService extends ApiService<Post> {}
