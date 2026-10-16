import os
import platform

def get_system_telemetry() -> dict:
    os_info = {}
    
    # Check mounted host OS release first, fallback to container release
    target_os_file = "/etc/host-os-release" if os.path.exists("/etc/host-os-release") else "/etc/os-release"
    
    if os.path.exists(target_os_file):
        with open(target_os_file) as f:
            for line in f:
                if "=" in line:
                    k, v = line.strip().split("=", 1)
                    os_info[k] = v.strip('"')

    os_id = os_info.get("ID", "").lower()
    os_like = os_info.get("ID_LIKE", "").lower()

    # Map host OS distribution to its native package managers
    if os_id in ["manjaro", "arch", "endeavouros", "garuda"] or "arch" in os_like:
        pkg_managers = ["pacman", "yay", "paru"]
    elif os_id in ["ubuntu", "debian", "pop", "mint"] or "debian" in os_like:
        pkg_managers = ["apt"]
    elif os_id in ["fedora", "rhel", "centos"] or "fedora" in os_like:
        pkg_managers = ["dnf"]
    else:
        pkg_managers = ["pacman"] if "manjaro" in os_info.get("NAME", "").lower() else ["apt"]

    return {
        "os_name": os_info.get("NAME", platform.system()),
        "os_id": os_id,
        "kernel": platform.release(),
        "architecture": platform.machine(),
        "package_managers": pkg_managers,
        "shell": "/bin/bash"
    }

if __name__ == "__main__":
    import json
    print(json.dumps(get_system_telemetry(), indent=2))
