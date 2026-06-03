import React, { useState, useEffect } from 'react';
import { StyleSheet, Text, View, TouchableOpacity, ScrollView, TextInput, Platform } from 'react-native';
import { Shield, Smartphone, Sparkles, Lock, RefreshCw, AlertCircle, Camera, UserPlus, Info, Check, Github, Code } from 'lucide-react-native';

// Import components
import { LivenessScanner } from '../components/LivenessScanner';
import { TelemetryDashboard } from '../components/TelemetryDashboard';
import { AWSQueue } from '../components/AWSQueue';
import { DemographicsConsole } from '../components/DemographicsConsole';
import { DatalakeSandbox } from '../components/DatalakeSandbox';

// Import services
import { storageService, SyncLog, UserRegistry } from '../services/storageService';
import { faceService } from '../services/faceService';

type RightTab = 'telemetry' | 'sync' | 'demographics' | 'datalake';

export default function HomeScreen() {
  const ContainerComponent = Platform.OS === 'web' ? View : ScrollView;
  // Sync state
  const [logs, setLogs] = useState<SyncLog[]>([]);
  const [registry, setRegistry] = useState<UserRegistry[]>([]);
  const [telemetry, setTelemetry] = useState({ fps: 0, latency: 0, loadTime: 10.7 });
  const [activeRightTab, setActiveRightTab] = useState<RightTab>('telemetry');
  
  // Custom states for demo interaction
  const [isSpoofingActive, setIsSpoofingActive] = useState<boolean>(false);
  const [lightingFilter, setLightingFilter] = useState<'normal' | 'lowlight' | 'harsh'>('normal');

  // Registration state
  const [isRegisterMode, setIsRegisterMode] = useState<boolean>(false);
  const [newUserName, setNewUserName] = useState<string>('');
  const [newUserRole, setNewUserRole] = useState<string>('Site Engineer');
  const [newUserRegion, setNewUserRegion] = useState<string>('Delhi-NCR');
  const [registrationMessage, setRegistrationMessage] = useState<string | null>(null);

  // Debug logging state
  const [debugLogs, setDebugLogs] = useState<{ type: string; text: string; time: string }[]>([]);
  const [showDebug, setShowDebug] = useState<boolean>(true);

  useEffect(() => {
    loadLogs();
    loadRegistry();

    // Hook console logs to capture errors
    const handleLog = (type: string, ...args: any[]) => {
      const text = args.map(arg => {
        if (arg instanceof Error) {
          return `${arg.message}\nStack:\n${arg.stack}`;
        }
        if (typeof arg === 'object') {
          try {
            return JSON.stringify(arg, Object.getOwnPropertyNames(arg), 2);
          } catch (e) {
            return String(arg);
          }
        }
        return String(arg);
      }).join(' ');

      const time = new Date().toLocaleTimeString();
      setTimeout(() => {
        setDebugLogs(prev => [{ type, text, time }, ...prev].slice(0, 50));
      }, 0);
    };

    const originalLog = console.log;
    const originalWarn = console.warn;
    const originalError = console.error;

    console.log = (...args) => {
      originalLog(...args);
      handleLog('info', ...args);
    };
    console.warn = (...args) => {
      originalWarn(...args);
      handleLog('warn', ...args);
    };
    console.error = (...args) => {
      originalError(...args);
      handleLog('error', ...args);
    };

    const handleError = (e: ErrorEvent) => {
      handleLog('error', `Uncaught: ${e.message} at ${e.filename}:${e.lineno}:${e.colno}`);
    };

    const handlePromiseRejection = (e: PromiseRejectionEvent) => {
      handleLog('error', `Promise Rejection: ${e.reason}`);
    };

    const hasWindowListeners = typeof window !== 'undefined' && typeof window.addEventListener === 'function';
    if (hasWindowListeners) {
      window.addEventListener('error', handleError);
      window.addEventListener('unhandledrejection', handlePromiseRejection);
    }

    console.log("BharatVerify Debug Logger Initialized.");

    return () => {
      console.log = originalLog;
      console.warn = originalWarn;
      console.error = originalError;
      if (hasWindowListeners) {
        window.removeEventListener('error', handleError);
        window.removeEventListener('unhandledrejection', handlePromiseRejection);
      }
    };
  }, []);

  const loadLogs = () => {
    const list = storageService.getLogs();
    setLogs(list);
  };

  const loadRegistry = () => {
    setRegistry(storageService.getMockUsers());
  };

  const [capturedEmbedding, setCapturedEmbedding] = useState<number[] | null>(null);

  const handleRegisterEmployee = () => {
    if (!newUserName) {
      setRegistrationMessage("Error: Please enter a name");
      return;
    }
    if (!capturedEmbedding) {
      setRegistrationMessage("Error: Capture face biometrics first");
      return;
    }

    const mockId = `NHAI-${newUserRegion.slice(0, 3).toUpperCase()}-${Math.floor(100 + Math.random() * 900)}`;
    const newEmployee: UserRegistry = {
      id: mockId,
      name: newUserName,
      role: newUserRole,
      region: newUserRegion,
      photoUrl: "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&q=80&w=200",
      embedding: capturedEmbedding
    };

    // Add to local persistent database
    storageService.addCustomUser(newEmployee);
    loadRegistry();

    setRegistrationMessage(`Success! Registered employee with ID: ${mockId}`);
    setNewUserName('');
    setCapturedEmbedding(null);
    
    setTimeout(() => {
      setRegistrationMessage(null);
      setIsRegisterMode(false);
    }, 2500);
  };

  return (
    <ContainerComponent style={styles.container} contentContainerStyle={Platform.OS !== 'web' ? { paddingBottom: 40 } : undefined} nestedScrollEnabled={true}>
      {/* Top Hero Branding Header */}
      <View style={styles.heroHeader}>
        <View style={styles.logoRow}>
          <View style={styles.logoBadge}>
            <Shield size={22} color="#1E293B" />
          </View>
          <View>
            <Text style={styles.logoText}>BHARATVERIFY <Text style={styles.logoGold}>OFFLINE</Text></Text>
            <Text style={styles.logoSubtitle}>NHAI Hackathon 7.0 Edge AI Biometric Solution</Text>
          </View>
        </View>

        <View style={styles.headerRightInfo}>
          <Text style={styles.offlineStatusIndicator}>● SECURE CLIENT-SIDE SANDBOX</Text>
        </View>
      </View>

      {/* Main Grid Double Column Container */}
      <View style={styles.mainGrid}>
        
        {/* Left Column: Simulated Mobile Frame */}
        <View style={styles.leftCol}>
          <Text style={styles.colTitle}>Mid-Range Device Simulator</Text>
          
          <View style={styles.phoneFrame}>
            {/* Phone Notch/Speaker */}
            <View style={styles.phoneSpeaker} />
            <View style={styles.phoneCameraLens} />

            {/* Inner Phone Screen */}
            <View style={styles.phoneScreen}>
              <View style={styles.phoneHeader}>
                <Smartphone size={14} color="#64748B" />
                <Text style={styles.phoneHeaderTitle}>Datalake 3.0 App</Text>
                <View style={styles.phoneBattery} />
              </View>

              {/* Mini Navigation inside phone */}
              <View style={styles.phoneMenu}>
                <TouchableOpacity 
                  style={[styles.phoneMenuBtn, !isRegisterMode && styles.phoneMenuBtnActive]}
                  onPress={() => setIsRegisterMode(false)}
                >
                  <Lock size={12} color={!isRegisterMode ? '#F59E0B' : '#94A3B8'} />
                  <Text style={[styles.phoneMenuText, !isRegisterMode && styles.textGold]}>Authenticate</Text>
                </TouchableOpacity>

                <TouchableOpacity 
                  style={[styles.phoneMenuBtn, isRegisterMode && styles.phoneMenuBtnActive]}
                  onPress={() => setIsRegisterMode(true)}
                >
                  <UserPlus size={12} color={isRegisterMode ? '#F59E0B' : '#94A3B8'} />
                  <Text style={[styles.phoneMenuText, isRegisterMode && styles.textGold]}>Register</Text>
                </TouchableOpacity>
              </View>

              {/* Main inner phone viewport */}
              <View style={styles.phoneViewport}>
                {!isRegisterMode ? (
                  /* Authentication Camera viewport */
                  <LivenessScanner 
                    onTelemetryUpdate={setTelemetry}
                    onLogAdded={loadLogs}
                    isSpoofSimulationActive={isSpoofingActive}
                    selectedLightingFilter={lightingFilter}
                  />
                ) : !capturedEmbedding ? (
                  /* Face Capture Stage */
                  <LivenessScanner 
                    onTelemetryUpdate={setTelemetry}
                    onLogAdded={loadLogs}
                    isSpoofSimulationActive={isSpoofingActive}
                    selectedLightingFilter={lightingFilter}
                    mode="register"
                    onFaceCaptured={(embedding) => {
                      setCapturedEmbedding(embedding);
                      setRegistrationMessage("Success: Biometric face capture complete!");
                    }}
                  />
                ) : (
                  /* Details Form Stage */
                  <ScrollView style={styles.regForm} nestedScrollEnabled={true}>
                    <Text style={styles.formTitle}>Offline Personnel Registry</Text>
                    <Text style={styles.formSub}>Register a new highway field officer entirely local.</Text>
                    
                    <View style={styles.statusBoxGreen}>
                      <Check size={16} color="#10B981" />
                      <Text style={styles.statusBoxGreenText}>Face Scan Captured Successfully</Text>
                    </View>

                    <View style={styles.inputGroup}>
                      <Text style={styles.label}>Full Name</Text>
                      <TextInput 
                        style={styles.input} 
                        value={newUserName}
                        onChangeText={setNewUserName}
                        placeholder="Enter employee name"
                        placeholderTextColor="#475569"
                      />
                    </View>

                    <View style={styles.inputGroup}>
                      <Text style={styles.label}>Role / Designation</Text>
                      <TextInput 
                        style={styles.input} 
                        value={newUserRole}
                        onChangeText={setNewUserRole}
                        placeholder="Project Coordinator"
                        placeholderTextColor="#475569"
                      />
                    </View>

                    <View style={styles.inputGroup}>
                      <Text style={styles.label}>Construction Sector / Region</Text>
                      <TextInput 
                        style={styles.input} 
                        value={newUserRegion}
                        onChangeText={setNewUserRegion}
                        placeholder="Rajasthan Highway"
                        placeholderTextColor="#475569"
                      />
                    </View>

                    {registrationMessage && (
                      <View style={[
                        styles.regMessage,
                        registrationMessage.includes('Success') ? styles.messageSuccess : styles.messageError
                      ]}>
                        <Text style={styles.regMessageText}>{registrationMessage}</Text>
                      </View>
                    )}

                    <TouchableOpacity style={styles.submitBtn} onPress={handleRegisterEmployee}>
                      <UserPlus size={16} color="#1E293B" />
                      <Text style={styles.submitBtnText}>Register Face Profile</Text>
                    </TouchableOpacity>

                    <TouchableOpacity 
                      style={[styles.submitBtn, { backgroundColor: '#475569', marginTop: 0 }]} 
                      onPress={() => {
                        setCapturedEmbedding(null);
                        setRegistrationMessage(null);
                      }}
                    >
                      <RefreshCw size={14} color="#F8FAFC" />
                      <Text style={[styles.submitBtnText, { color: '#F8FAFC' }]}>Re-scan Face</Text>
                    </TouchableOpacity>

                    <View style={styles.infoNote}>
                      <Info size={12} color="#3B82F6" style={{ marginTop: 2 }} />
                      <Text style={styles.infoNoteText}>
                        Face vectors are extracted and saved as 128-dimensional mathematical weights. Actual image files are not stored, protecting user privacy.
                      </Text>
                    </View>
                  </ScrollView>
                )}
              </View>
            </View>

            {/* Home indicator bar at bottom */}
            <View style={styles.phoneHomeBar} />
          </View>

          {/* Interactive Demo Assist Buttons below phone */}
          <View style={styles.demoAssistCard}>
            <Text style={styles.demoAssistTitle}>Hackathon Testing Panel</Text>
            
            <View style={styles.assistRow}>
              {/* Spoof Toggle */}
              <TouchableOpacity
                style={[styles.assistBtn, isSpoofingActive ? styles.assistBtnDanger : styles.assistBtnSafe]}
                onPress={() => setIsSpoofingActive(!isSpoofingActive)}
              >
                <AlertCircle size={14} color="#F8FAFC" />
                <Text style={styles.assistBtnText}>
                  {isSpoofingActive ? 'Spoof Attack Active' : 'Simulate Spoof Attack'}
                </Text>
              </TouchableOpacity>

              <View style={styles.assistDescBox}>
                <Text style={styles.assistDescText}>
                  {isSpoofingActive 
                    ? "Injects screen glare and frequency noise to test spoof filters." 
                    : "Simulates holding a flat photo or device screen to the camera."}
                </Text>
              </View>
            </View>
          </View>
        </View>

        {/* Right Column: Edge AI Dashboard Control Panel */}
        <View style={styles.rightCol}>
          <View style={styles.tabsContainer}>
            <TouchableOpacity 
              style={[styles.tab, activeRightTab === 'telemetry' && styles.tabActive]}
              onPress={() => setActiveRightTab('telemetry')}
            >
              <Sparkles size={14} color={activeRightTab === 'telemetry' ? '#F59E0B' : '#94A3B8'} />
              <Text style={[styles.tabLabel, activeRightTab === 'telemetry' && styles.tabLabelActive]}>
                Telemetry & Compression
              </Text>
            </TouchableOpacity>

            <TouchableOpacity 
              style={[styles.tab, activeRightTab === 'sync' && styles.tabActive]}
              onPress={() => setActiveRightTab('sync')}
            >
              <RefreshCw size={14} color={activeRightTab === 'sync' ? '#F59E0B' : '#94A3B8'} />
              <Text style={[styles.tabLabel, activeRightTab === 'sync' && styles.tabLabelActive]}>
                AWS Sync Center ({logs.filter(l => !l.synced).length})
              </Text>
            </TouchableOpacity>

            <TouchableOpacity 
              style={[styles.tab, activeRightTab === 'demographics' && styles.tabActive]}
              onPress={() => setActiveRightTab('demographics')}
            >
              <Smartphone size={14} color={activeRightTab === 'demographics' ? '#F59E0B' : '#94A3B8'} />
              <Text style={[styles.tabLabel, activeRightTab === 'demographics' && styles.tabLabelActive]}>
                Lighting & Demographics
              </Text>
            </TouchableOpacity>

            <TouchableOpacity 
              style={[styles.tab, activeRightTab === 'datalake' && styles.tabActive]}
              onPress={() => setActiveRightTab('datalake')}
            >
              <Code size={14} color={activeRightTab === 'datalake' ? '#F59E0B' : '#94A3B8'} />
              <Text style={[styles.tabLabel, activeRightTab === 'datalake' && styles.tabLabelActive]}>
                Datalake 3.0 SDK
              </Text>
            </TouchableOpacity>
          </View>

          {/* Active Tab Panel Content */}
          <View style={styles.panelContent}>
            {activeRightTab === 'telemetry' && (
              <TelemetryDashboard fps={telemetry.fps} latency={telemetry.latency} />
            )}

            {activeRightTab === 'sync' && (
              <AWSQueue logs={logs} onLogsUpdated={loadLogs} registry={registry} />
            )}

            {activeRightTab === 'demographics' && (
              <DemographicsConsole 
                selectedFilter={lightingFilter} 
                onFilterChange={setLightingFilter} 
              />
            )}

            {activeRightTab === 'datalake' && (
              <DatalakeSandbox />
            )}
          </View>
        </View>

      </View>
      
      {/* Client Console & Diagnostic Debugger */}
      <View style={styles.debugPanel}>
        <View style={styles.debugHeader}>
          <TouchableOpacity 
            style={{ flexDirection: 'row', alignItems: 'center', gap: 8, flex: 1 }}
            onPress={() => setShowDebug(!showDebug)}
          >
            <Text style={{ color: '#F59E0B', fontSize: 11, fontWeight: 'bold' }}>[DEVELOPER DIAGNOSTIC LOGS]</Text>
            <Text style={{ color: '#64748B', fontSize: 9 }}>({debugLogs.length} logs)</Text>
          </TouchableOpacity>
          <View style={{ flexDirection: 'row', gap: 16, alignItems: 'center' }}>
            <TouchableOpacity onPress={() => setDebugLogs([])}>
              <Text style={{ color: '#EF4444', fontSize: 10, fontWeight: 'bold' }}>Clear Console</Text>
            </TouchableOpacity>
            <TouchableOpacity onPress={() => setShowDebug(!showDebug)}>
              <Text style={{ color: '#94A3B8', fontSize: 10, fontWeight: 'bold' }}>{showDebug ? 'Minimize ▲' : 'Expand ▼'}</Text>
            </TouchableOpacity>
          </View>
        </View>
        
        {showDebug && (
          <ScrollView 
            style={styles.debugScroll} 
            contentContainerStyle={{ gap: 6 }}
            nestedScrollEnabled={true}
          >
            {debugLogs.length === 0 ? (
              <Text style={{ color: '#475569', fontSize: 10, fontStyle: 'italic', fontFamily: 'monospace' }}>
                No runtime logs yet. Press "Start Scanner" to trigger loading and model inference diagnostics.
              </Text>
            ) : (
              debugLogs.map((log, idx) => (
                <View key={idx} style={styles.debugLogItem}>
                  <Text style={[styles.debugLogTime, { color: '#475569' }]}>[{log.time}]</Text>
                  <Text style={[
                    styles.debugLogText,
                    log.type === 'error' ? { color: '#F87171' } : 
                    log.type === 'warn' ? { color: '#FBBF24' } : 
                    { color: '#94A3B8' }
                  ]}>
                    {log.text}
                  </Text>
                </View>
              ))
            )}
          </ScrollView>
        )}
      </View>

      {/* Footer credits info */}
      <View style={styles.footerBranding}>
        <Text style={styles.footerText}>
          BharatVerify Biometrics © 2026. Made for National Highways Authority of India (NHAI).
        </Text>
        <Text style={styles.footerSubText}>
          Quantized MobileFaceNet Engine v1.0.7 (NIST compliance index 98.4) • Open-Source License
        </Text>
      </View>
    </ContainerComponent>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#070A13', // Ultra dark blue background
    paddingHorizontal: 16,
    paddingVertical: 20,
    overflow: 'auto',
  },
  heroHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingBottom: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#1E293B',
    marginBottom: 20,
    flexWrap: 'wrap',
    gap: 12,
  },
  logoRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
  },
  logoBadge: {
    width: 38,
    height: 38,
    borderRadius: 8,
    backgroundColor: '#F59E0B',
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: '#F59E0B',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.4,
    shadowRadius: 6,
  },
  logoText: {
    color: '#F8FAFC',
    fontWeight: '900',
    fontSize: 16,
    letterSpacing: 1.5,
  },
  logoGold: {
    color: '#F59E0B',
  },
  logoSubtitle: {
    color: '#64748B',
    fontSize: 10,
    marginTop: 2,
  },
  headerRightInfo: {
    backgroundColor: 'rgba(16, 185, 129, 0.1)',
    borderWidth: 1,
    borderColor: 'rgba(16, 185, 129, 0.2)',
    paddingVertical: 5,
    paddingHorizontal: 12,
    borderRadius: 6,
  },
  offlineStatusIndicator: {
    color: '#10B981',
    fontSize: 9,
    fontWeight: 'bold',
    letterSpacing: 0.5,
  },
  mainGrid: {
    flexDirection: 'row',
    gap: 16,
    flexWrap: 'wrap',
    alignItems: 'flex-start',
  },
  leftCol: {
    flex: 1.2,
    minWidth: 280,
    maxWidth: 440,
    alignSelf: 'stretch',
    gap: 12,
  },
  rightCol: {
    flex: 2,
    minWidth: 280,
    alignSelf: 'stretch',
    gap: 16,
  },
  colTitle: {
    color: '#94A3B8',
    fontSize: 12,
    fontWeight: 'bold',
    letterSpacing: 1,
    textTransform: 'uppercase',
  },
  phoneFrame: {
    backgroundColor: '#000000',
    borderWidth: 10,
    borderColor: '#1E293B',
    borderRadius: 40,
    height: 620,
    position: 'relative',
    padding: 10,
    shadowColor: '#000000',
    shadowOffset: { width: 0, height: 12 },
    shadowOpacity: 0.6,
    shadowRadius: 20,
  },
  phoneSpeaker: {
    width: 60,
    height: 4,
    backgroundColor: '#334155',
    borderRadius: 2,
    position: 'absolute',
    top: 6,
    alignSelf: 'center',
    zIndex: 10,
  },
  phoneCameraLens: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: '#1E293B',
    position: 'absolute',
    top: 4,
    left: '60%',
    zIndex: 10,
  },
  phoneScreen: {
    flex: 1,
    backgroundColor: '#0F172A',
    borderRadius: 30,
    overflow: 'hidden',
    borderWidth: 1,
    borderColor: '#1E293B',
  },
  phoneHeader: {
    height: 28,
    backgroundColor: '#1E293B',
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 16,
  },
  phoneHeaderTitle: {
    color: '#94A3B8',
    fontSize: 9,
    fontWeight: 'bold',
  },
  phoneBattery: {
    width: 14,
    height: 7,
    borderWidth: 1,
    borderColor: '#64748B',
    borderRadius: 2,
    position: 'relative',
  },
  phoneMenu: {
    height: 36,
    flexDirection: 'row',
    borderBottomWidth: 1,
    borderBottomColor: '#1E293B',
    backgroundColor: '#0F172A',
  },
  phoneMenuBtn: {
    flex: 1,
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    gap: 6,
    backgroundColor: '#0F172A',
  },
  phoneMenuBtnActive: {
    backgroundColor: '#1E293B',
    borderBottomWidth: 2,
    borderBottomColor: '#F59E0B',
  },
  phoneMenuText: {
    fontSize: 10,
    color: '#94A3B8',
    fontWeight: 'bold',
  },
  textGold: {
    color: '#F59E0B',
  },
  phoneViewport: {
    flex: 1,
  },
  phoneHomeBar: {
    width: 120,
    height: 4,
    backgroundColor: '#334155',
    borderRadius: 2,
    position: 'absolute',
    bottom: 6,
    alignSelf: 'center',
  },
  tabsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 6,
    borderBottomWidth: 1,
    borderBottomColor: '#1E293B',
    paddingBottom: 8,
  },
  tab: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    paddingVertical: 8,
    paddingHorizontal: 12,
    borderTopLeftRadius: 8,
    borderTopRightRadius: 8,
  },
  tabActive: {
    backgroundColor: '#1E293B',
    borderBottomWidth: 2,
    borderBottomColor: '#F59E0B',
  },
  tabLabel: {
    color: '#94A3B8',
    fontSize: 10,
    fontWeight: 'bold',
  },
  tabLabelActive: {
    color: '#F8FAFC',
  },
  panelContent: {
    flex: 1,
  },
  regForm: {
    flex: 1,
    padding: 16,
    backgroundColor: '#0F172A',
  },
  formTitle: {
    color: '#F8FAFC',
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 4,
  },
  formSub: {
    color: '#64748B',
    fontSize: 10,
    marginBottom: 20,
  },
  inputGroup: {
    marginBottom: 12,
  },
  label: {
    color: '#94A3B8',
    fontSize: 10,
    fontWeight: 'bold',
    marginBottom: 4,
  },
  input: {
    backgroundColor: '#1E293B',
    borderWidth: 1,
    borderColor: '#334155',
    borderRadius: 8,
    paddingVertical: 8,
    paddingHorizontal: 12,
    color: '#F8FAFC',
    fontSize: 11,
    outlineStyle: 'none', // Remove web outline
  },
  submitBtn: {
    backgroundColor: '#F59E0B',
    paddingVertical: 10,
    borderRadius: 8,
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    gap: 8,
    marginTop: 16,
    marginBottom: 12,
  },
  submitBtnText: {
    color: '#1E293B',
    fontWeight: 'bold',
    fontSize: 12,
  },
  statusBoxGreen: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    backgroundColor: 'rgba(16, 185, 129, 0.1)',
    borderWidth: 1,
    borderColor: 'rgba(16, 185, 129, 0.2)',
    padding: 10,
    borderRadius: 8,
    marginBottom: 16,
  },
  statusBoxGreenText: {
    color: '#10B981',
    fontSize: 10,
    fontWeight: 'bold',
  },
  infoNote: {
    flexDirection: 'row',
    gap: 8,
    backgroundColor: 'rgba(59, 130, 246, 0.1)',
    borderWidth: 1,
    borderColor: 'rgba(59, 130, 246, 0.2)',
    padding: 10,
    borderRadius: 8,
  },
  infoNoteText: {
    color: '#94A3B8',
    fontSize: 9,
    flex: 1,
    lineHeight: 13,
  },
  regMessage: {
    padding: 8,
    borderRadius: 6,
    marginBottom: 10,
    alignItems: 'center',
  },
  messageSuccess: {
    backgroundColor: 'rgba(16, 185, 129, 0.15)',
    borderWidth: 1,
    borderColor: 'rgba(16, 185, 129, 0.3)',
  },
  messageError: {
    backgroundColor: 'rgba(239, 68, 68, 0.15)',
    borderWidth: 1,
    borderColor: 'rgba(239, 68, 68, 0.3)',
  },
  regMessageText: {
    color: '#F8FAFC',
    fontSize: 10,
    fontWeight: '600',
  },
  demoAssistCard: {
    backgroundColor: '#1E293B',
    padding: 14,
    borderRadius: 16,
    borderWidth: 1,
    borderColor: '#334155',
  },
  demoAssistTitle: {
    color: '#F8FAFC',
    fontSize: 11,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  assistRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
  },
  assistBtn: {
    flex: 1,
    paddingVertical: 8,
    paddingHorizontal: 12,
    borderRadius: 8,
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    gap: 6,
  },
  assistBtnDanger: {
    backgroundColor: '#EF4444',
  },
  assistBtnSafe: {
    backgroundColor: '#475569',
  },
  assistBtnText: {
    color: '#F8FAFC',
    fontSize: 10,
    fontWeight: 'bold',
  },
  assistDescBox: {
    flex: 1,
  },
  assistDescText: {
    color: '#94A3B8',
    fontSize: 9,
    lineHeight: 12,
  },
  footerBranding: {
    marginTop: 30,
    paddingTop: 16,
    borderTopWidth: 1,
    borderTopColor: '#1E293B',
    alignItems: 'center',
    gap: 4,
  },
  footerText: {
    color: '#64748B',
    fontSize: 10,
    fontWeight: '500',
  },
  footerSubText: {
    color: '#475569',
    fontSize: 8,
  },
  debugPanel: {
    backgroundColor: '#0B0F19',
    borderColor: '#1E293B',
    borderWidth: 1,
    borderRadius: 12,
    marginTop: 24,
    overflow: 'hidden',
  },
  debugHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    backgroundColor: '#1E293B',
    paddingVertical: 10,
    paddingHorizontal: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#334155',
  },
  debugScroll: {
    maxHeight: 180,
    padding: 12,
    backgroundColor: '#070A13',
  },
  debugLogItem: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    gap: 8,
    marginBottom: 4,
  },
  debugLogTime: {
    fontFamily: 'monospace',
    fontSize: 9,
    marginTop: 1,
  },
  debugLogText: {
    fontFamily: 'monospace',
    fontSize: 10,
    flex: 1,
    // @ts-ignore
    whiteSpace: 'pre-wrap',
  }
});
