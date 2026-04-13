import Foundation

struct NotionCase: Identifiable, Decodable, Hashable {
    let id: String
    let name: String
    let status: String
    let merchant: String
    let followUpDate: String?

    enum CodingKeys: String, CodingKey {
        case id, name, status, merchant
        case followUpDate = "follow_up_date"
    }

    static func from(json: [String: Any]) -> NotionCase? {
        guard
            let id       = json["id"] as? String,
            let name     = json["name"] as? String,
            let status   = json["status"] as? String,
            let merchant = json["merchant"] as? String
        else { return nil }
        return NotionCase(
            id: id,
            name: name,
            status: status,
            merchant: merchant,
            followUpDate: json["follow_up_date"] as? String
        )
    }

    var statusColor: String {
        switch status.lowercased() {
        case "done", "complete", "launched": return "green"
        case "blocked", "cancelled":         return "red"
        case "in progress", "active":        return "blue"
        default:                             return "gray"
        }
    }
}
