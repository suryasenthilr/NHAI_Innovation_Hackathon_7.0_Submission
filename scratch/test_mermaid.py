import base64
import urllib.request
import sys

def test():
    # Diagram 6 with quoted labels
    diagram = """stateDiagram-v2
    [*] --> ScreenIdle: "Mount Component"
    ScreenIdle --> ScreenScanning: "Click 'Start Scanner'"
    ScreenScanning --> RunPassiveChecks: "Capture Video Frame"
    
    state RunPassiveChecks {
        [*] --> TextureCheck: "Compute Laplacian Grayscale Variance"
        TextureCheck --> FailCheck: "Variance < 15.0 (Printed Spoof)"
        TextureCheck --> GlowCheck: "Variance >= 15.0"
        GlowCheck --> FailCheck: "RGB Red-to-Blue Ratio < 1.02 (Screen Replay)"
        GlowCheck --> PassPassive: "Ratio >= 1.02"
    }
    
    RunPassiveChecks --> ScreenLockout: "Fails Passive Checks"
    RunPassiveChecks --> SelectActiveChallenge: "Passes Passive Checks"
    
    state SelectActiveChallenge {
        [*] --> RandomizeChallenge: "Select [Blink, Smile, Yaw]"
        RandomizeChallenge --> ChallengeBlink: "Prompt: 'Blink Your Eyes'"
        RandomizeChallenge --> ChallengeSmile: "Prompt: 'Smile to Verify'"
        RandomizeChallenge --> ChallengeYaw: "Prompt: 'Turn Head Left/Right'"
        
        ChallengeBlink --> VerificationSuccess: "EAR < 0.25 within 6s"
        ChallengeSmile --> VerificationSuccess: "Ratio > 0.75 within 6s"
        ChallengeYaw --> VerificationSuccess: "Yaw Ratio < 0.72 or > 1.40 within 6s"
        
        ChallengeBlink --> Timeout: "Seconds > 6.0"
        ChallengeSmile --> Timeout: "Seconds > 6.0"
        ChallengeYaw --> Timeout: "Seconds > 6.0"
        
        Timeout --> RandomizeChallenge: "Try Next Challenge"
    }
    
    SelectActiveChallenge --> ScreenLockout: "3 Failed Active Challenges"
    SelectActiveChallenge --> GenerateFaceEmbedding: "Success"
    
    GenerateFaceEmbedding --> LocalRegistryMatch: "128-D Euclidean Vector extracted"
    LocalRegistryMatch --> ScreenAuthenticated: "Distance d < 0.60 (Match Found)"
    LocalRegistryMatch --> ScreenAccessDenied: "Distance d >= 0.60"
    
    ScreenAuthenticated --> SyncStaging: "Cache Record Offline in SQLite"
    SyncStaging --> SyncProcessing: "Reconnect Online -> AWS POST trigger"
    SyncProcessing --> [*]: "AWS 200 OK Handshake -> Local auto-purge" """
    
    # URLsafe Base64 encode
    graph_bytes = diagram.encode("utf-8")
    base64_bytes = base64.urlsafe_b64encode(graph_bytes)
    base64_string = base64_bytes.decode("ascii")
    
    url = f"https://mermaid.ink/svg/{base64_string}"
    print(f"Fetching from: {url}")
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            svg_data = response.read()
            print("Successfully downloaded SVG!")
            print(f"SVG size: {len(svg_data)} bytes")
    except Exception as e:
        print(f"Error fetching SVG: {e}", file=sys.stderr)

if __name__ == "__main__":
    test()
