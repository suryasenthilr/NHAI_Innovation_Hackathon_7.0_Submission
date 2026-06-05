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
    # Test 1: Simple state diagram
    try_mermaid("""stateDiagram-v2
    [*] --> ScreenIdle
    ScreenIdle --> [*]""", "Test 1: Simple diagram")

    # Test 2: Compound state
    try_mermaid("""stateDiagram-v2
    state RunPassiveChecks {
        [*] --> TextureCheck
        TextureCheck --> GlowCheck
    }""", "Test 2: Compound state")

    # Test 3: Transitions with special characters
    try_mermaid("""stateDiagram-v2
    state RunPassiveChecks {
        [*] --> TextureCheck
        TextureCheck --> FailCheck: Variance < 15.0
        GlowCheck --> FailCheck: RGB Ratio < 1.02
    }""", "Test 3: Special characters in labels")

    # Test 4: Nested states and transitions outside
    try_mermaid("""stateDiagram-v2
    state SelectActiveChallenge {
        [*] --> RandomizeChallenge
        ChallengeBlink --> VerificationSuccess: EAR < 0.25 within 6s
    }
    SelectActiveChallenge --> GenerateFaceEmbedding: Success""", "Test 4: Nested and outside transitions")

    # Test 5: The complete Diagram 6 but with minimal labels
    try_mermaid("""stateDiagram-v2
    [*] --> ScreenIdle
    ScreenIdle --> ScreenScanning
    ScreenScanning --> RunPassiveChecks
    
    state RunPassiveChecks {
        [*] --> TextureCheck
        TextureCheck --> FailCheck
        TextureCheck --> GlowCheck
        GlowCheck --> FailCheck
        GlowCheck --> PassPassive
    }
    
    RunPassiveChecks --> ScreenLockout
    RunPassiveChecks --> SelectActiveChallenge
    
    state SelectActiveChallenge {
        [*] --> RandomizeChallenge
        RandomizeChallenge --> ChallengeBlink
        RandomizeChallenge --> ChallengeSmile
        RandomizeChallenge --> ChallengeYaw
        
        ChallengeBlink --> VerificationSuccess
        ChallengeSmile --> VerificationSuccess
        ChallengeYaw --> VerificationSuccess
        
        ChallengeBlink --> Timeout
        ChallengeSmile --> Timeout
        ChallengeYaw --> Timeout
        
        Timeout --> RandomizeChallenge
    }
    
    SelectActiveChallenge --> ScreenLockout
    SelectActiveChallenge --> GenerateFaceEmbedding
    
    GenerateFaceEmbedding --> LocalRegistryMatch
    LocalRegistryMatch --> ScreenAuthenticated
    LocalRegistryMatch --> ScreenAccessDenied
    
    ScreenAuthenticated --> SyncStaging
    SyncStaging --> SyncProcessing
    SyncProcessing --> [*]""", "Test 5: Full Diagram 6 without labels")

if __name__ == "__main__":
    test()
