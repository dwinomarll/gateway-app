import Foundation

struct ChatMessage: Identifiable {
    enum Role { case user, assistant }

    let id     = UUID()
    let role:    Role
    let content: String
    let ts:      Date

    init(role: Role, content: String) {
        self.role    = role
        self.content = content
        self.ts      = Date()
    }

    var isUser: Bool { role == .user }
}
