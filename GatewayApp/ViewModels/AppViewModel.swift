import Foundation
import SwiftUI

@MainActor
final class AppViewModel: ObservableObject {
    @Published var health:   HealthStatus?
    @Published var cases:    [NotionCase]  = []
    @Published var messages: [ChatMessage] = []
    @Published var chatInput: String       = ""
    @Published var isSending: Bool         = false
    @Published var errorBanner: String?

    private var wsTask: URLSessionWebSocketTask?

    var badgeCount: Int { cases.filter { $0.status.lowercased() == "in progress" }.count }
    var healthColor: Color { health?.overallColor ?? .gray }

    func boot() {
        Task { await refreshHealth() }
        Task { await refreshCases() }
        Task {
            wsTask = await GatewayClient.shared.connectWebSocket { [weak self] status in
                Task { @MainActor [weak self] in self?.health = status }
            }
        }
    }

    func refreshHealth() async {
        do    { health = try await GatewayClient.shared.fetchHealth() }
        catch { errorBanner = "Health check failed" }
    }

    func refreshCases() async {
        do    { cases = try await GatewayClient.shared.fetchCases() }
        catch { errorBanner = "Could not load Notion cases" }
    }

    func sendMessage() async {
        let text = chatInput.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !text.isEmpty else { return }
        chatInput = ""
        messages.append(ChatMessage(role: .user, content: text))
        isSending = true
        do {
            let reply = try await GatewayClient.shared.sendChat(message: text)
            messages.append(ChatMessage(role: .assistant, content: reply))
        } catch {
            messages.append(ChatMessage(role: .assistant, content: "⚠️ \(error.localizedDescription)"))
        }
        isSending = false
    }
}
