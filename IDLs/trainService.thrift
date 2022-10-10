namespace cpp trainService

struct AuthDto {
    1: string value
}

service tsUserService {
    string createDefaultUser(1:AuthDto dto)
}

service tsAuthService {
    string verifyCode(1:string code, 2:string req)
}