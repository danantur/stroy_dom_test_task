import axios from "axios"

const back_url = location.protocol + '//' + location.hostname + ":3001"

export class Service {

    constructor (path) {
        this.path = path
    }

    getData() {
        return axios.get(`${back_url}/${this.path}`);
    }

    delete(id) {
        return axios.delete(`${back_url}/${this.path}/${id}`)
    }

    deleteMany(objects) {
        let promises = []
        for (let i in objects) {
            let object = objects[i]
            promises.push(this.delete(object.id))
        }
        return Promise.all(promises)
    }

    add(object) {
        return axios.post(`${back_url}/${this.path}`, object)
    }

    update(object) {
        return axios.put(`${back_url}/${this.path}/${object.id}`, object)
    }

    getAllMini() {
        return Promise.resolve(this.getData().slice(0, 5));
    }

    getAllSmall() {
        return Promise.resolve(this.getData().slice(0, 10));
    }

    getAll() {
        return Promise.resolve(this.getData());
    }

}