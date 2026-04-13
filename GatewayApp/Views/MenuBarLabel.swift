import SwiftUI

struct MenuBarLabel: View {
    @EnvironmentObject var vm: AppViewModel

    var body: some View {
        HStack(spacing: 4) {
            Circle()
                .fill(vm.healthColor)
                .frame(width: 8, height: 8)
            if vm.badgeCount > 0 {
                Text("\(vm.badgeCount)")
                    .font(.system(size: 11, weight: .semibold))
            }
        }
    }
}
