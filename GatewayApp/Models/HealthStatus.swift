import Foundation
import SwiftUI

struct HealthStatus: Decodable {
    enum ServiceStatus: String, Decodable {
        case ok, down, degraded
    }

    let openclaw: ServiceStatus
    let n8n: ServiceStatus
    let shift4: ServiceStatus

    var overallColor: Color {
        let statuses = [openclaw, n8n, shift4]
        if statuses.contains(.down)     { return .red }
        if statuses.contains(.degraded) { return .yellow }
        return .green
    }

    var summary: String {
        "\(openclaw.rawValue) / \(n8n.rawValue) / \(shift4.rawValue)"
    }
}
