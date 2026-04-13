import Foundation

actor GatewayClient {
    static let shared = GatewayClient()
    private let base = URL(string: "http://localhost:9191")!

    // MARK: — REST

    func fetchHealth() async throws -> HealthStatus {
        let (data, _) = try await URLSession.shared.data(from: base.appending(path: "/health"))
        return try JSONDecoder().decode(HealthStatus.self, from: data)
    }

    func fetchCases() async throws -> [NotionCase] {
        let (data, _) = try await URLSession.shared.data(from: base.appending(path: "/notion"))
        let raw = try JSONSerialization.jsonObject(with: data) as? [[String: Any]] ?? []
        return raw.compactMap(NotionCase.from)
    }

    func sendChat(message: String) async throws -> String {
        var req          = URLRequest(url: base.appending(path: "/chat"))
        req.httpMethod   = "POST"
        req.setValue("application/json", forHTTPHeaderField: "Content-Type")
        req.httpBody     = try JSONSerialization.data(withJSONObject: ["message": message])
        let (data, _)    = try await URLSession.shared.data(for: req)
        let json         = try JSONSerialization.jsonObject(with: data) as? [String: Any]
        return json?["reply"] as? String
            ?? json?["content"] as? String
            ?? "…"
    }

    // MARK: — WebSocket

    func connectWebSocket(onMessage: @escaping (HealthStatus) -> Void) -> URLSessionWebSocketTask {
        var components   = URLComponents(url: base.appending(path: "/ws"), resolvingAgainstBaseURL: false)!
        components.scheme = "ws"
        let task          = URLSession.shared.webSocketTask(with: components.url!)
        task.resume()
        receiveLoop(task: task, onMessage: onMessage)
        return task
    }

    private func receiveLoop(task: URLSessionWebSocketTask, onMessage: @escaping (HealthStatus) -> Void) {
        task.receive { result in
            guard case .success(let msg) = result else { return }
            if case .string(let text) = msg,
               let data   = text.data(using: .utf8),
               let payload = try? JSONDecoder().decode([String: AnyCodable].self, from: data),
               payload["type"]?.value as? String == "health",
               let raw    = try? JSONSerialization.data(withJSONObject: payload["data"]?.value as Any),
               let status = try? JSONDecoder().decode(HealthStatus.self, from: raw) {
                onMessage(status)
            }
            self.receiveLoop(task: task, onMessage: onMessage)
        }
    }
}

// Minimal AnyCodable for WS payload parsing
struct AnyCodable: Codable {
    let value: Any
    init(_ value: Any) { self.value = value }
    init(from decoder: Decoder) throws {
        let c = try decoder.singleValueContainer()
        if let s = try? c.decode(String.self)  { value = s; return }
        if let i = try? c.decode(Int.self)     { value = i; return }
        if let d = try? c.decode(Double.self)  { value = d; return }
        if let b = try? c.decode(Bool.self)    { value = b; return }
        if let a = try? c.decode([AnyCodable].self) { value = a.map(\.value); return }
        if let o = try? c.decode([String: AnyCodable].self) { value = o.mapValues(\.value); return }
        value = ""
    }
    func encode(to encoder: Encoder) throws {
        var c = encoder.singleValueContainer()
        switch value {
        case let s as String: try c.encode(s)
        case let i as Int:    try c.encode(i)
        case let d as Double: try c.encode(d)
        case let b as Bool:   try c.encode(b)
        default: try c.encodeNil()
        }
    }
}
