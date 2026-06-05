import base64
import urllib.request
import sys

def try_mermaid(code, description):
    graph_bytes = code.encode("utf-8")
    base64_bytes = base64.urlsafe_b64encode(graph_bytes)
    base64_string = base64_bytes.decode("ascii")
    url = f"https://mermaid.ink/svg/{base64_string}"
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            svg_data = r.read()
            print(f"SUCCESS {description}: ({len(svg_data)} bytes)")
            return True
    except Exception as e:
        print(f"FAILED {description}: ({e})")
        return False

def test():
    diagram = """stateDiagram-v2
    [*] --> ScreenIdle: Mount Component
    ScreenIdle --> ScreenScanning: Click Start Scanner
    ScreenScanning --> RunPassiveChecks: Capture Video Frame
    
    state RunPassiveChecks {
        [*] --> TextureCheck: Compute Laplacian Grayscale Variance
        TextureCheck --> FailCheck: Variance less than 15.0
        TextureCheck --> GlowCheck: Variance at least 15.0
        GlowCheck --> FailCheck: RGB Ratio less than 1.02
        GlowCheck --> PassPassive: Ratio at least 1.02
    }
    
    RunPassiveChecks --> ScreenLockout: Fails Passive Checks
    RunPassiveChecks --> SelectActiveChallenge: Passes Passive Checks
    
    state SelectActiveChallenge {
        [*] --> RandomizeChallenge: Select Blink Smile or Yaw
        RandomizeChallenge --> ChallengeBlink: Prompt Blink Your Eyes
        RandomizeChallenge --> ChallengeSmile: Prompt Smile to Verify
        RandomizeChallenge --> ChallengeYaw: Prompt Turn Head Left or Right
        
        ChallengeBlink --> VerificationSuccess: EAR less than 0.25 within 6s
        ChallengeSmile --> VerificationSuccess: Ratio greater than 0.75 within 6s
        ChallengeYaw --> VerificationSuccess: Yaw Ratio out of bounds within 6s
        
        ChallengeBlink --> Timeout: Seconds greater than 6.0
        ChallengeSmile --> Timeout: Seconds greater than 6.0
        ChallengeYaw --> Timeout: Seconds greater than 6.0
        
        Timeout --> RandomizeChallenge: Try Next Challenge
    }
    
    SelectActiveChallenge --> ScreenLockout: 3 Failed Active Challenges
    SelectActiveChallenge --> GenerateFaceEmbedding: Success
    
    GenerateFaceEmbedding --> LocalRegistryMatch: 128-D Euclidean Vector extracted
    LocalRegistryMatch --> ScreenAuthenticated: Distance less than 0.60
    LocalRegistryMatch --> ScreenAccessDenied: Distance at least 0.60
    
    ScreenAuthenticated --> SyncStaging: Cache Record Offline in SQLite
    SyncStaging --> SyncProcessing: Reconnect Online then AWS POST trigger
    SyncProcessing --> [*]: AWS 200 OK Handshake then Local auto-purge"""
    
    try_mermaid(diagram, "Full Diagram 6 with clean alphanumeric labels")

if __name__ == "__main__":
    test()
