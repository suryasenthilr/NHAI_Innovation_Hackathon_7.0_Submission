export interface LogDetails {
  blinkPassed: boolean;
  smilePassed: boolean;
  headPassed: boolean;
}

export interface SyncLog {
  id: string;
  userId: string;
  userName: string;
  timestamp: string;
  status: 'SUCCESS' | 'FAILED';
  livenessScore: number;
  matchScore: number;
  gpsCoords: {
    latitude: number;
    longitude: number;
  };
  verificationMode: 'OFFLINE';
  synced: boolean;
  deviceModel: string;
  livenessDetails: LogDetails;
  spoofAttemptDetected: boolean;
}

export interface UserRegistry {
  id: string;
  name: string;
  role: string;
  region: string;
  photoUrl: string;
  // Simulated 128D facial embedding vector (mocked for matching baseline)
  embedding: number[];
}

const DEFAULT_REGISTRY: UserRegistry[] = [
  {
    id: "NHAI-DEL-EXAMPLE",
    name: "Amit Sharma (Example - Mock Data)",
    role: "Project Manager",
    region: "Delhi-NCR",
    photoUrl: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&q=80&w=200",
    embedding: new Array(128).fill(0).map((_, i) => Math.sin(i * 0.1) * 0.5 + 0.1)
  }
];

const STORAGE_KEY_LOGS = 'nhai_liveness_offline_logs';

class StorageService {
  private logs: SyncLog[] = [];

  private customAwsUrl: string | null = null;

  private customUsers: UserRegistry[] = [];

  constructor() {
    this.loadLogs();
    this.loadCustomAwsUrl();
    this.loadRegistry();
  }

  private loadRegistry() {
    try {
      if (typeof window !== 'undefined' && window.localStorage) {
        const stored = window.localStorage.getItem('nhai_user_registry');
        if (stored) {
          this.customUsers = JSON.parse(stored);
          return;
        }
      }
    } catch (e) {
      console.error("Failed to load user registry", e);
    }
    this.customUsers = [];
  }

  private saveRegistry() {
    try {
      if (typeof window !== 'undefined' && window.localStorage) {
        window.localStorage.setItem('nhai_user_registry', JSON.stringify(this.customUsers));
      }
    } catch (e) {
      console.error("Failed to save user registry", e);
    }
  }

  private loadLogs() {
    try {
      if (typeof window !== 'undefined' && window.localStorage) {
        const stored = window.localStorage.getItem(STORAGE_KEY_LOGS);
        if (stored) {
          this.logs = JSON.parse(stored);
          return;
        }
      }
      this.logs = [];
    } catch (e) {
      console.error("Failed to load logs from storage", e);
      this.logs = [];
    }
  }

  private loadCustomAwsUrl() {
    try {
      if (typeof window !== 'undefined' && window.localStorage) {
        this.customAwsUrl = window.localStorage.getItem('nhai_custom_aws_url');
      }
    } catch (e) {
      console.error("Failed to load custom AWS URL", e);
    }
  }

  public setCustomAwsUrl(url: string | null) {
    this.customAwsUrl = url;
    try {
      if (typeof window !== 'undefined' && window.localStorage) {
        if (url) {
          window.localStorage.setItem('nhai_custom_aws_url', url);
        } else {
          window.localStorage.removeItem('nhai_custom_aws_url');
        }
      }
    } catch (e) {
      console.error("Failed to save custom AWS URL", e);
    }
  }

  public getCustomAwsUrl(): string | null {
    return this.customAwsUrl;
  }

  private saveLogs() {
    try {
      if (typeof window !== 'undefined' && window.localStorage) {
        window.localStorage.setItem(STORAGE_KEY_LOGS, JSON.stringify(this.logs));
      }
    } catch (e) {
      console.error("Failed to save logs to storage", e);
    }
  }

  public getMockUsers(): UserRegistry[] {
    return [...DEFAULT_REGISTRY, ...this.customUsers];
  }

  public addCustomUser(user: UserRegistry) {
    this.customUsers.push(user);
    this.saveRegistry();
  }

  public getLogs(): SyncLog[] {
    this.loadLogs();
    return this.logs;
  }

  public addLog(log: Omit<SyncLog, 'id' | 'synced'>): SyncLog {
    this.loadLogs();
    const newLog: SyncLog = {
      ...log,
      id: `LOG-${Date.now()}-${Math.floor(Math.random() * 1000)}`,
      synced: false
    };
    this.logs.unshift(newLog);
    this.saveLogs();
    return newLog;
  }

  public async syncWithAWS(): Promise<{ successCount: number; failedCount: number; isLive: boolean; error?: string }> {
    this.loadLogs();
    const pendingLogs = this.logs.filter(l => !l.synced);
    if (pendingLogs.length === 0) return { successCount: 0, failedCount: 0, isLive: false };

    // If a custom AWS Lambda URL is configured, push live data!
    if (this.customAwsUrl) {
      try {
        console.log(`[AWS Live Sync] Sending ${pendingLogs.length} logs to ${this.customAwsUrl}`);
        const response = await fetch(this.customAwsUrl, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(pendingLogs)
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log("[AWS Live Sync Success]", data);

        // Mark as synced locally
        this.logs = this.logs.map(log => {
          if (!log.synced) {
            return { ...log, synced: true };
          }
          return log;
        });
        this.saveLogs();

        return {
          successCount: pendingLogs.length,
          failedCount: 0,
          isLive: true
        };
      } catch (error: any) {
        console.error("[AWS Live Sync Failed]", error);
        return {
          successCount: 0,
          failedCount: pendingLogs.length,
          isLive: true,
          error: error.message || String(error)
        };
      }
    } else {
      // Offline Simulation Fallback
      await new Promise(resolve => setTimeout(resolve, 1500));

      this.logs = this.logs.map(log => {
        if (!log.synced) {
          return { ...log, synced: true };
        }
        return log;
      });
      this.saveLogs();

      return {
        successCount: pendingLogs.length,
        failedCount: 0,
        isLive: false
      };
    }
  }

  public purgeSyncedLogs(): number {
    this.loadLogs();
    const beforeCount = this.logs.length;
    this.logs = this.logs.filter(l => !l.synced);
    const purgedCount = beforeCount - this.logs.length;
    this.saveLogs();
    return purgedCount;
  }

  public clearAllLogs() {
    this.logs = [];
    this.saveLogs();
  }
}

export const storageService = new StorageService();
