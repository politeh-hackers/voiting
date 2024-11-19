export interface BaseUUIDSchema {
    id: string,
}

export interface Error {
    error: string
}

export class ApiService<T> {
    baseUrl: string = "http://localhost:8000"

    public async getAll(prefix: string): Promise<T[]> {
        const response = await fetch(`${this.baseUrl}/${prefix}`);
        const jsonData = await response.json()
        return jsonData as T[]
    }

    public async create(data: T, prefix: string): Promise<void | Error> {
        const response = await fetch(`${this.baseUrl}/${prefix}`, {
            body: JSON.stringify(data)
        });
        if (response.status !== 200) {
            return await response.json() as Error
        }
        return
    }
}

export interface Post extends BaseUUIDSchema {
    title: string
}

export class PostService extends ApiService<Post> {}
