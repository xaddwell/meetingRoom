import request from '../util/request'


export function QueryMeetingForUser() {
  return request({
    url: 'http://127.0.0.1:8000/meeting/QueryMeetingForUser',
    method: 'get',
	params:{'username':window.sessionStorage.getItem('username')}
  })
}

export function QueryAllMeetings() {
  return request({
    url: 'http://127.0.0.1:8000/meeting/QueryAllMeetings',
    method: 'get',
	params:{'username':window.sessionStorage.getItem('username')}
  })
}


export function QueryAllRoom() {
  return request({
    url: 'http://127.0.0.1:8000/meeting/QueryAllRoom',
    method: 'get',
	params:{'username':window.sessionStorage.getItem('username')}
  })
}




export function QuerymyRoomChartoption() {
  return request({
    url: 'http://127.0.0.1:8000/meeting/QuerymyRoomChartoption',
    method: 'get',
	params:{'username':window.sessionStorage.getItem('username')}
  })
}


export function QuerymyChartoption() {
  return request({
    url: 'http://127.0.0.1:8000/meeting/QuerymyChartoption',
    method: 'get',
	params:{'username':window.sessionStorage.getItem('username')}
  })
}


