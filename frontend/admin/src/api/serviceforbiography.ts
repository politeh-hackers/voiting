export interface BaseUUIDSchema {
    id?: string,
}

export interface Error {
    error: string
}

export class ApiService<T> {
    baseUrl: string = "http://localhost:8000"
    

    public async getAll(prefix: string, baseAdmin:string): Promise<T[]> {
        const response = await fetch(`${this.baseUrl}/${baseAdmin}/${prefix}`);
        const jsonData = await response.json()
        return jsonData as T[]
    }

    public async create(data: T | FormData, prefix: string, baseAdmin:string): Promise<void | Error> {
        
        const response = await fetch(`${this.baseUrl}/${baseAdmin}/${prefix}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json', // Указание типа контента
            },
            body: JSON.stringify(data)
        });
        if (response.status !== 200) {
            return await response.json() as Error
        }
        return response.json() ;
    }
    public async delete(prefix: string,id: string, baseAdmin:string):Promise<void>{
        const response = await fetch(`${this.baseUrl}/${baseAdmin}/${prefix}/${id}`,{
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json', // Указание типа контента
            },
            
        });
    }
    public async patch(prefix: string,id: string, baseAdmin:string, data:T):Promise<void>{
        const response = await fetch(`${this.baseUrl}/${baseAdmin}/${prefix}/${id}`,{
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json', // Указание типа контента
            },
            body: JSON.stringify(data)
        })
    }
}

export interface Post extends BaseUUIDSchema {
    h1:string
    title:string
    description:string
    header:string
    main_photo:string
    content:string
    date_created:Date
}

export class PostService extends ApiService<Post> {}
