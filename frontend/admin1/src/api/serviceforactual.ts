export interface BaseUUIDSchema {
    id?: string,
}

export interface Error {
    error: string
}

export class ApiService<T> {
    baseUrl: string = "http://localhost:8000"
    token: string

    constructor(token: string) {
        this.token = token;
    }

    protected getHeaders(isFormData: boolean = false): HeadersInit {
        const headers: HeadersInit = {
            'Authorization': this.token
        };
        
        if (!isFormData) {
            headers['Content-Type'] = 'application/json';
        }
        
        return headers;
    }

    public async getAll(prefix: string, baseAdmin: string): Promise<T[]> {
        const response = await fetch(`${this.baseUrl}/${baseAdmin}/${prefix}`, {
            headers: this.getHeaders()
        });
        const jsonData = await response.json()
        return jsonData as T[]
    }

    public async create(data: T | FormData, prefix: string, baseAdmin: string): Promise<void | Error> {
        const isFormData = data instanceof FormData;
        const response = await fetch(`${this.baseUrl}/${baseAdmin}/${prefix}`, {
            method: 'POST',
            headers: this.getHeaders(isFormData),
            body: isFormData ? data : JSON.stringify(data)
        });
        if (response.status !== 200) {
            return await response.json() as Error
        }
        return response.json();
    }

    public async delete(prefix: string, id: string): Promise<void> {
        const response = await fetch(`${this.baseUrl}/${prefix}/${id}`, {
            method: 'DELETE',
            headers: this.getHeaders()
        });
    }

    public async patch(prefix: string, id: string,  data: T): Promise<void> {
        const response = await fetch(`${this.baseUrl}/${prefix}/${id}`, {
            method: 'PATCH',
            headers: this.getHeaders(),
            body: JSON.stringify(data)
        });
    }

    public async deleteImage(imageName: string): Promise<void> {
        const response = await fetch(`${this.baseUrl}/admin/image/${imageName}`, {
            method: 'DELETE',
            headers: this.getHeaders(),
            body: JSON.stringify({ file_url: `${this.baseUrl}/static/image/${imageName}` })
        });

        if (!response.ok) {
            throw new Error("Ошибка при удалении изображения");
        }
    }
}

export interface Post extends BaseUUIDSchema {
    slug: string
    h1: string
    title: string
    description: string
    header: string
    summary: string
    main_photo: string
    content: string
    date_created: any
}

export class PostService extends ApiService<Post> {
    async loadPosts(): Promise<Post[]> {
        return this.getAll('actual', 'actual');
    }

    async createPost(postData: FormData): Promise<void | Error> {
        return this.create(postData, 'actual', 'actual');
    }

    async updatePost(id: string, postData: Post): Promise<void> {
        return this.patch('actual', id, postData);
    }

    async deletePost(id: string): Promise<void> {
        return this.delete('actual', id);
    }

    getImageNameFromUrl(fileUrl: string): string {
        return fileUrl.split("/").pop() || '';
    }

    async deleteImage(fileUrl: string): Promise<void> {
        const imageName = this.getImageNameFromUrl(fileUrl);
        return super.deleteImage(imageName);
    }
}
