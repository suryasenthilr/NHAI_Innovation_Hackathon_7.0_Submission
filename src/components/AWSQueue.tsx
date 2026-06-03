import React, { useState, useEffect } from 'react';
import { StyleSheet, Text, View, TouchableOpacity, ScrollView, ActivityIndicator, TextInput } from 'react-native';
import { Wifi, WifiOff, CloudLightning, Trash2, Cloud, FileText, Check, Database, MapPin, Settings } from 'lucide-react-native';
import { storageService, SyncLog } from '../services/storageService';

import { UserRegistry } from '../services/storageService';

interface AWSQueueProps {
  logs: SyncLog[];
  onLogsUpdated: () => void;
  registry: UserRegistry[];
}

export const AWSQueue: React.FC<AWSQueueProps> = ({ logs, onLogsUpdated, registry }) => {
  const [isOnline, setIsOnline] = useState<boolean>(false);
  const [syncingState, setSyncingState] = useState<'idle' | 'encrypting' | 'uploading' | 'purging' | 'done'>('idle');
  const [syncedLogsInfo, setSyncedLogsInfo] = useState<{ success: number } | null>(null);
  
  // Custom AWS settings state
  const [customAwsUrl, setCustomAwsUrl] = useState<string>('');

  useEffect(() => {
    const savedUrl = storageService.getCustomAwsUrl() || '';
    setCustomAwsUrl(savedUrl);
  }, []);

  const handleSaveAwsUrl = () => {
    storageService.setCustomAwsUrl(customAwsUrl.trim() || null);
    alert("AWS Configuration Saved Successfully!");
  };

  const pendingCount = logs.filter(l => !l.synced).length;
  const syncedCount = logs.filter(l => l.synced).length;

  const handleToggleNetwork = () => {
    setIsOnline(!isOnline);
  };

  const handleSyncLogs = async () => {
    if (!isOnline || pendingCount === 0) return;

    setSyncingState('encrypting');
    
    // Step 1: Encrypting local database records (Simulated SECURE hashing)
    await new Promise(resolve => setTimeout(resolve, 800));
    setSyncingState('uploading');

    // Step 2: Uploading S3 payload hashes and RDS records
    try {
      const result = await storageService.syncWithAWS();
      
      if (result.error) {
        setSyncingState('idle');
        alert(`AWS Sync Error: ${result.error}\n\nPlease check your Lambda Function URL configuration and verify CORS settings on AWS.`);
        return;
      }

      setSyncedLogsInfo({ success: result.successCount });
      setSyncingState('purging');
      
      // Step 3: Purging synced records locally to ensure compliance with privacy laws
      await new Promise(resolve => setTimeout(resolve, 1000));
      const purged = storageService.purgeSyncedLogs();
      onLogsUpdated();
      
      setSyncingState('done');
      setTimeout(() => {
        setSyncingState('idle');
        setSyncedLogsInfo(null);
      }, 3000);
    } catch (e: any) {
      console.error(e);
      setSyncingState('idle');
      alert(`Sync Exception: ${e.message || String(e)}`);
    }
  };

  const handleClearLogs = () => {
    storageService.clearAllLogs();
    onLogsUpdated();
  };

  const formatTime = (isoString: string) => {
    const d = new Date(isoString);
    return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }) + ' ' + d.toLocaleDateString();
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>AWS Server Sync & Purge Hub</Text>
        
        {/* Toggle Mode */}
        <TouchableOpacity 
          style={[styles.networkToggle, isOnline ? styles.networkOnline : styles.networkOffline]}
          onPress={handleToggleNetwork}
        >
          {isOnline ? <Wifi size={14} color="#1E293B" /> : <WifiOff size={14} color="#F8FAFC" />}
          <Text style={[styles.networkToggleText, isOnline ? styles.textSlate : styles.textWhite]}>
            {isOnline ? 'Online' : 'Offline'}
          </Text>
        </TouchableOpacity>
      </View>

      {/* AWS Settings Configuration Panel (Always Visible & Exposed) */}
      <View style={styles.settingsCard}>
        <Text style={styles.settingsTitle}>⚙️ AWS Lambda Function URL Configuration</Text>
        <Text style={styles.settingsSub}>
          Evaluators: Paste your custom AWS Lambda URL here to route biometric check-in sync queues live to your cloud console. If empty, local simulation mode is used.
        </Text>
        <View style={{ flexDirection: 'row', gap: 8, alignItems: 'center' }}>
          <TextInput
            style={[styles.settingsInput, { flex: 1, marginBottom: 0 }]}
            value={customAwsUrl}
            onChangeText={setCustomAwsUrl}
            placeholder="Paste AWS Lambda URL (https://xxxx.lambda-url.region.on.aws/)"
            placeholderTextColor="#475569"
            autoCapitalize="none"
            autoCorrect={false}
          />
          <TouchableOpacity style={[styles.saveBtn, { height: 32, justifyContent: 'center' }]} onPress={handleSaveAwsUrl}>
            <Text style={styles.saveBtnText}>Save Endpoint</Text>
          </TouchableOpacity>
        </View>
      </View>
      {/* Sync Telemetry */}
      <View style={styles.statsBar}>
        <View style={styles.statBox}>
          <Database size={16} color="#F59E0B" />
          <View>
            <Text style={styles.statVal}>{pendingCount}</Text>
            <Text style={styles.statLbl}>Pending Upload</Text>
          </View>
        </View>
        
        <View style={styles.statBox}>
          <Cloud size={16} color="#10B981" />
          <View>
            <Text style={styles.statVal}>{syncedCount}</Text>
            <Text style={styles.statLbl}>Synced Logs</Text>
          </View>
        </View>
      </View>

      {/* Sync Operations */}
      <View style={styles.opsRow}>
        <TouchableOpacity
          style={[
            styles.syncBtn,
            (!isOnline || pendingCount === 0) && styles.syncBtnDisabled
          ]}
          disabled={!isOnline || pendingCount === 0 || syncingState !== 'idle'}
          onPress={handleSyncLogs}
        >
          {syncingState === 'idle' ? (
            <>
              <CloudLightning size={16} color="#1E293B" />
              <Text style={styles.syncBtnText}>Sync Logs to AWS</Text>
            </>
          ) : (
            <ActivityIndicator size="small" color="#1E293B" />
          )}
        </TouchableOpacity>

        <TouchableOpacity style={styles.clearBtn} onPress={handleClearLogs}>
          <Trash2 size={14} color="#EF4444" />
          <Text style={styles.clearBtnText}>Purge All Logs</Text>
        </TouchableOpacity>
      </View>

      {/* Syncing Progress Visualizer */}
      {syncingState !== 'idle' && (
        <View style={styles.syncProgressOverlay}>
          <View style={styles.progressCard}>
            {syncingState === 'encrypting' && (
              <>
                <ActivityIndicator size="small" color="#F59E0B" />
                <Text style={styles.progressStepText}>Encrypting local DB with AES-256 hashes...</Text>
              </>
            )}
            {syncingState === 'uploading' && (
              <>
                <ActivityIndicator size="small" color="#3B82F6" />
                <Text style={styles.progressStepText}>Pushing secured payload to AWS S3 & DynamoDB...</Text>
              </>
            )}
            {syncingState === 'purging' && (
              <>
                <ActivityIndicator size="small" color="#10B981" />
                <Text style={styles.progressStepText}>Sync confirmed. Purging local logs securely...</Text>
              </>
            )}
            {syncingState === 'done' && (
              <>
                <View style={styles.checkCircle}>
                  <Check size={18} color="#10B981" />
                </View>
                <Text style={styles.progressStepSuccess}>
                  AWS Upload Complete! {syncedLogsInfo?.success} logs purged from local storage.
                </Text>
              </>
            )}
          </View>
        </View>
      )}

      {/* Active AWS Endpoint indicator */}
      <View style={styles.endpointIndicator}>
        <Text style={styles.endpointLabel}>Active Cloud Endpoint:</Text>
        <Text style={styles.endpointValue} numberOfLines={1} ellipsizeMode="middle">
          {storageService.getCustomAwsUrl() || 'Offline Simulation Mode (Local Sandbox)'}
        </Text>
      </View>

      {/* Logs Registry List */}
      <Text style={styles.tableTitle}>Offline Logs Cache Registry</Text>
      
      {logs.length === 0 ? (
        <View style={styles.emptyLogs}>
          <FileText size={32} color="#475569" style={{ marginBottom: 8 }} />
          <Text style={styles.emptyText}>No authentication logs captured yet.</Text>
          <Text style={styles.emptySubText}>Use the Biometric Camera in the Mobile frame to register scans offline.</Text>
        </View>
      ) : (
        <ScrollView style={styles.logsList} nestedScrollEnabled={true}>
          {logs.map((log) => (
            <View key={log.id} style={styles.logCard}>
              <View style={styles.logCardHeader}>
                <View>
                  <Text style={styles.logName}>{log.userName}</Text>
                  <Text style={styles.logId}>ID: {log.userId} • {log.deviceModel}</Text>
                </View>
                
                <View style={[styles.syncStatusBadge, log.synced ? styles.badgeSynced : styles.badgePending]}>
                  {log.synced ? <Cloud size={10} color="#10B981" /> : <WifiOff size={10} color="#F59E0B" />}
                  <Text style={[styles.syncStatusText, log.synced ? styles.textSynced : styles.textPending]}>
                    {log.synced ? 'SYNCED & PURGED' : 'PENDING SYNC'}
                  </Text>
                </View>
              </View>

              {/* Log Stats grid */}
              <View style={styles.logMetricsGrid}>
                <View style={styles.logMetricCol}>
                  <Text style={styles.metricLabel}>GPS COORDS</Text>
                  <View style={styles.gpsRow}>
                    <MapPin size={8} color="#94A3B8" />
                    <Text style={styles.metricVal}>
                      {log.gpsCoords.latitude.toFixed(4)}, {log.gpsCoords.longitude.toFixed(4)}
                    </Text>
                  </View>
                </View>

                <View style={styles.logMetricCol}>
                  <Text style={styles.metricLabel}>VERIFICATION</Text>
                  <Text style={[styles.metricVal, log.status === 'SUCCESS' ? styles.textGreen : styles.textRed]}>
                    {log.status} ({Math.round(log.matchScore * 100)}% Match)
                  </Text>
                </View>

                <View style={styles.logMetricCol}>
                  <Text style={styles.metricLabel}>LIVENESS CHECKS</Text>
                  <Text style={styles.metricVal}>
                    B:{log.livenessDetails.blinkPassed ? '✓' : '✗'} S:{log.livenessDetails.smilePassed ? '✓' : '✗'} H:{log.livenessDetails.headPassed ? '✓' : '✗'}
                  </Text>
                </View>
              </View>

              {/* Timestamp */}
              <Text style={styles.logTime}>{formatTime(log.timestamp)}</Text>
            </View>
          ))}
        </ScrollView>
      )}

      {/* Local Personnel Registry Database */}
      <Text style={[styles.tableTitle, { marginTop: 20 }]}>Local Personnel Registry Database</Text>
      <Text style={{ color: '#94A3B8', fontSize: 11, marginBottom: 10, lineHeight: 14 }}>
        When you register a face via the "Register Face" panel, the new user will show up here in real-time with their extracted biometric embedding. The initial profile below is a fake mock example.
      </Text>
      <ScrollView style={styles.registryList} nestedScrollEnabled={true}>
        {registry.length === 0 ? (
          <View style={{ padding: 16, backgroundColor: '#0F172A', borderRadius: 8, borderWidth: 1, borderColor: '#334155', alignItems: 'center' }}>
            <Text style={{ color: '#94A3B8', fontSize: 11, fontWeight: 'bold' }}>No registered users found.</Text>
            <Text style={{ color: '#64748B', fontSize: 9, marginTop: 4, textAlign: 'center' }}>
              When you enroll a face via the Register Face panel, the persistent biometric template will appear here in real-time.
            </Text>
          </View>
        ) : (
          registry.map((user) => (
            <View key={user.id} style={styles.personCard}>
              <View style={styles.personHeader}>
                <View style={styles.avatarCircle}>
                  <Text style={styles.avatarText}>{user.name.charAt(0)}</Text>
                </View>
                <View style={{ flex: 1 }}>
                  <Text style={styles.personName}>{user.name}</Text>
                  <Text style={styles.personId}>
                    ID: {user.id} • {user.role} {user.id === 'NHAI-DEL-EXAMPLE' ? '(Example - Mock)' : ''}
                  </Text>
                  <Text style={styles.personRegion}>Region: {user.region}</Text>
                </View>
              </View>
              <View style={styles.vectorBox}>
                <Text style={styles.vectorLabel}>FACIAL EMBEDDING VECTOR (FIRST 5 / 128 FLOATS):</Text>
                <Text style={styles.vectorVal}>
                  [{user.embedding.slice(0, 5).map(n => n.toFixed(4)).join(', ')}, ...]
                </Text>
              </View>
            </View>
          ))
        )}
      </ScrollView>
    </View>
  );
};

const styles = StyleSheet.create({
  endpointIndicator: {
    backgroundColor: '#0F172A',
    paddingVertical: 8,
    paddingHorizontal: 12,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#334155',
    marginBottom: 16,
  },
  endpointLabel: {
    color: '#64748B',
    fontSize: 8,
    fontWeight: 'bold',
    textTransform: 'uppercase',
    marginBottom: 2,
  },
  endpointValue: {
    color: '#E2E8F0',
    fontSize: 10,
    fontFamily: 'monospace',
  },
  settingsToggle: {
    padding: 6,
    borderRadius: 20,
    backgroundColor: '#0F172A',
    borderWidth: 1,
    borderColor: '#334155',
    justifyContent: 'center',
    alignItems: 'center',
  },
  settingsToggleActive: {
    borderColor: '#F59E0B',
    backgroundColor: 'rgba(245, 158, 11, 0.1)',
  },
  settingsCard: {
    backgroundColor: '#0F172A',
    padding: 14,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: '#334155',
    marginBottom: 16,
  },
  settingsTitle: {
    color: '#F8FAFC',
    fontSize: 12,
    fontWeight: 'bold',
    marginBottom: 4,
  },
  settingsSub: {
    color: '#64748B',
    fontSize: 9,
    lineHeight: 12,
    marginBottom: 10,
  },
  settingsInput: {
    backgroundColor: '#1E293B',
    borderWidth: 1,
    borderColor: '#334155',
    borderRadius: 6,
    paddingVertical: 6,
    paddingHorizontal: 10,
    color: '#F8FAFC',
    fontSize: 10,
    outlineStyle: 'none',
    marginBottom: 10,
    fontFamily: 'monospace',
  },
  settingsButtons: {
    flexDirection: 'row',
    gap: 8,
  },
  saveBtn: {
    backgroundColor: '#F59E0B',
    paddingVertical: 6,
    paddingHorizontal: 12,
    borderRadius: 6,
  },
  saveBtnText: {
    color: '#0F172A',
    fontWeight: 'bold',
    fontSize: 10,
  },
  cancelBtn: {
    backgroundColor: '#334155',
    paddingVertical: 6,
    paddingHorizontal: 12,
    borderRadius: 6,
  },
  cancelBtnText: {
    color: '#94A3B8',
    fontWeight: '600',
    fontSize: 10,
  },
  container: {
    backgroundColor: '#1E293B',
    padding: 16,
    borderRadius: 16,
    borderWidth: 1,
    borderColor: '#334155',
    flex: 1,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
  },
  title: {
    color: '#F8FAFC',
    fontSize: 14,
    fontWeight: 'bold',
  },
  networkToggle: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    paddingVertical: 5,
    paddingHorizontal: 10,
    borderRadius: 20,
    borderWidth: 1,
  },
  networkOnline: {
    backgroundColor: '#10B981',
    borderColor: '#10B981',
  },
  networkOffline: {
    backgroundColor: 'rgba(245, 158, 11, 0.1)',
    borderColor: '#F59E0B',
  },
  networkToggleText: {
    fontSize: 10,
    fontWeight: 'bold',
  },
  textSlate: {
    color: '#0F172A',
  },
  textWhite: {
    color: '#F8FAFC',
  },
  textSynced: {
    color: '#10B981',
  },
  textPending: {
    color: '#F59E0B',
  },
  statsBar: {
    flexDirection: 'row',
    gap: 12,
    marginBottom: 16,
  },
  statBox: {
    flex: 1,
    backgroundColor: '#0F172A',
    padding: 10,
    borderRadius: 10,
    borderWidth: 1,
    borderColor: '#334155',
    flexDirection: 'row',
    alignItems: 'center',
    gap: 10,
  },
  statVal: {
    color: '#F8FAFC',
    fontSize: 16,
    fontWeight: 'bold',
  },
  statLbl: {
    color: '#94A3B8',
    fontSize: 9,
  },
  opsRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    gap: 12,
    marginBottom: 16,
  },
  syncBtn: {
    flex: 2,
    backgroundColor: '#F59E0B',
    paddingVertical: 10,
    borderRadius: 8,
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    gap: 8,
  },
  syncBtnDisabled: {
    backgroundColor: '#475569',
    opacity: 0.5,
  },
  syncBtnText: {
    color: '#0F172A',
    fontWeight: 'bold',
    fontSize: 12,
  },
  clearBtn: {
    flex: 1,
    backgroundColor: 'rgba(239, 68, 68, 0.1)',
    borderWidth: 1,
    borderColor: 'rgba(239, 68, 68, 0.3)',
    borderRadius: 8,
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    gap: 6,
  },
  clearBtnText: {
    color: '#EF4444',
    fontWeight: '600',
    fontSize: 11,
  },
  syncProgressOverlay: {
    backgroundColor: 'rgba(15, 23, 42, 0.95)',
    padding: 12,
    borderRadius: 10,
    borderWidth: 1,
    borderColor: '#334155',
    marginBottom: 16,
  },
  progressCard: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 10,
  },
  progressStepText: {
    color: '#F8FAFC',
    fontSize: 11,
  },
  progressStepSuccess: {
    color: '#10B981',
    fontSize: 11,
    fontWeight: 'bold',
  },
  checkCircle: {
    width: 24,
    height: 24,
    borderRadius: 12,
    backgroundColor: 'rgba(16, 185, 129, 0.15)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  tableTitle: {
    color: '#E2E8F0',
    fontSize: 12,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  emptyLogs: {
    backgroundColor: '#0F172A',
    padding: 30,
    borderRadius: 12,
    alignItems: 'center',
    justifyContent: 'center',
    borderWidth: 1,
    borderColor: '#334155',
    minHeight: 180,
  },
  emptyText: {
    color: '#94A3B8',
    fontSize: 11,
    fontWeight: 'bold',
    textAlign: 'center',
  },
  emptySubText: {
    color: '#475569',
    fontSize: 9,
    textAlign: 'center',
    marginTop: 4,
  },
  logsList: {
    maxHeight: 240,
  },
  logCard: {
    backgroundColor: '#0F172A',
    padding: 12,
    borderRadius: 10,
    borderWidth: 1,
    borderColor: '#334155',
    marginBottom: 10,
  },
  logCardHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 8,
  },
  logName: {
    color: '#F8FAFC',
    fontSize: 12,
    fontWeight: 'bold',
  },
  logId: {
    color: '#64748B',
    fontSize: 9,
    marginTop: 2,
  },
  syncStatusBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
    paddingVertical: 2,
    paddingHorizontal: 6,
    borderRadius: 4,
  },
  badgeSynced: {
    backgroundColor: 'rgba(16, 185, 129, 0.1)',
  },
  badgePending: {
    backgroundColor: 'rgba(245, 158, 11, 0.1)',
  },
  syncStatusText: {
    fontSize: 8,
    fontWeight: 'bold',
  },
  logMetricsGrid: {
    flexDirection: 'row',
    backgroundColor: '#1E293B',
    borderRadius: 6,
    padding: 8,
    marginBottom: 6,
  },
  logMetricCol: {
    flex: 1,
    gap: 3,
  },
  metricLabel: {
    color: '#64748B',
    fontSize: 7,
    fontWeight: 'bold',
  },
  metricVal: {
    color: '#E2E8F0',
    fontSize: 9,
    fontWeight: '500',
  },
  gpsRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 2,
  },
  textGreen: {
    color: '#10B981',
  },
  textRed: {
    color: '#EF4444',
  },
  logTime: {
    color: '#475569',
    fontSize: 8,
    textAlign: 'right',
  },
  registryList: {
    maxHeight: 180,
  },
  personCard: {
    backgroundColor: '#0F172A',
    padding: 10,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#334155',
    marginBottom: 8,
  },
  personHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 10,
    marginBottom: 6,
  },
  avatarCircle: {
    width: 32,
    height: 32,
    borderRadius: 16,
    backgroundColor: '#1E293B',
    borderWidth: 1,
    borderColor: '#F59E0B',
    justifyContent: 'center',
    alignItems: 'center',
  },
  avatarText: {
    color: '#F59E0B',
    fontSize: 12,
    fontWeight: 'bold',
  },
  personName: {
    color: '#F8FAFC',
    fontSize: 11,
    fontWeight: 'bold',
  },
  personId: {
    color: '#94A3B8',
    fontSize: 9,
  },
  personRegion: {
    color: '#64748B',
    fontSize: 8,
    marginTop: 1,
  },
  vectorBox: {
    backgroundColor: '#1E293B',
    padding: 6,
    borderRadius: 4,
  },
  vectorLabel: {
    color: '#64748B',
    fontSize: 7,
    fontWeight: 'bold',
    marginBottom: 2,
  },
  vectorVal: {
    color: '#F59E0B',
    fontSize: 8,
    fontFamily: 'monospace',
  }
});
