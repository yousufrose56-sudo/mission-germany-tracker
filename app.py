import { useRef, useSyncExternalStore } from "react";
import { buildDocumentList } from "./docList";
import { renderAgreement } from "./agreement";

export type Role = "admin" | "team" | "student";
export type DocStatus = "Pending" | "Uploaded" | "Approved" | "Rejected" | "Needs Correction";
export type Category = "Masters" | "Bachelors" | "MPG" | "DPG";
export type Gender = "Male" | "Female";

export interface User {
  id: string;
  email: string;
  password: string;
  role: Role;
  name: string;
  mustChangePassword?: boolean;
  studentId?: string;
}

export interface PassportInfo {
  fullName: string;
  dob: string;
  placeOfBirth: string;
  nationality: string;
  passportNumber: string;
  issueDate: string;
  expiryDate: string;
}

export interface Student {
  id: string;
  userId: string;
  category: Category;
  gender?: Gender;
  intake?: string;
  stage?: string;
  assignedTeamId?: string;
  onboardingComplete: boolean;
  onboardingStep: number; // 1..3
  passport?: PassportInfo;
  personal: Record<string, string>;
  academic: Record<string, string>;
  certifications: Record<string, string>;
  professional: Record<string, string>;
  program: Record<string, string>;
  agreement?: { acceptedAt: string; signature: string; html: string };
  createdAt: number;
  lastActivity: number;
}

export interface DocItem {
  id: string;
  studentId: string;
  stage: string;
  name: string;
  status: DocStatus;
  fileName?: string;
  dataUrl?: string;
  notes?: string;
  updatedAt: number;
}

export interface Note {
  id: string;
  studentId: string;
  authorId: string;
  authorName: string;
  text: string;
  createdAt: number;
}

export interface Payment {
  id: string;
  studentId: string;
  type: "registration" | "admission" | "other";
  label: string;
  amount: number;
  status: "Pending" | "Paid";
  paidAt?: number;
}

export interface AppState {
  users: User[];
  students: Student[];
  docs: DocItem[];
  notes: Note[];
  payments: Payment[];
  currentUserId: string | null;
}

const STORAGE_KEY = "mg-crm:v1";

const seedUsers: User[] = [
  { id: "u-admin", email: "admin@missiongermany.com", password: "admin123", role: "admin", name: "Admin User" },
  { id: "u-team", email: "team@missiongermany.com", password: "team123", role: "team", name: "Priya (Team)" },
  { id: "u-team2", email: "rahul@missiongermany.com", password: "team123", role: "team", name: "Rahul (Team)" },
];

const defaultState: AppState = {
  users: seedUsers,
  students: [],
  docs: [],
  notes: [],
  payments: [],
  currentUserId: null,
};

function load(): AppState {
  if (typeof window === "undefined") return defaultState;
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return defaultState;
    const parsed = JSON.parse(raw);
    // Always ensure seed admin/team exist
    const merged = { ...defaultState, ...parsed };
    for (const u of seedUsers) {
      if (!merged.users.find((x: User) => x.id === u.id)) merged.users.push(u);
    }
    return merged;
  } catch {
    return defaultState;
  }
}

let state: AppState = load();
const listeners = new Set<() => void>();

function persist() {
  if (typeof window === "undefined") return;
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
}

function setState(updater: (s: AppState) => AppState) {
  state = updater(state);
  persist();
  listeners.forEach((l) => l());
}

export function useAppState<T>(selector: (s: AppState) => T): T {
  const cache = useRef<{ state: AppState | null; value: T }>({ state: null, value: undefined as T });
  const getSnapshot = () => {
    if (cache.current.state !== state) {
      const next = selector(state);
      if (!shallowEqual(cache.current.value, next)) {
        cache.current = { state, value: next };
      } else {
        cache.current.state = state;
      }
    }
    return cache.current.value;
  };
  const serverCache = useRef<T | null>(null);
  const getServerSnapshot = () => {
    if (serverCache.current === null) serverCache.current = selector(defaultState);
    return serverCache.current as T;
  };
  return useSyncExternalStore(
    (cb) => {
      listeners.add(cb);
      return () => listeners.delete(cb);
    },
    getSnapshot,
    getServerSnapshot,
  );
}

function shallowEqual(a: unknown, b: unknown): boolean {
  if (Object.is(a, b)) return true;
  if (Array.isArray(a) && Array.isArray(b)) {
    if (a.length !== b.length) return false;
    for (let i = 0; i < a.length; i++) if (!Object.is(a[i], b[i])) return false;
    return true;
  }
  return false;
}

export function getState() {
  return state;
}

const uid = () => (typeof crypto !== "undefined" && crypto.randomUUID ? crypto.randomUUID() : Math.random().toString(36).slice(2));

export const auth = {
  login(email: string, password: string): User | null {
    const user = state.users.find((u) => u.email.toLowerCase() === email.toLowerCase() && u.password === password);
    if (!user) return null;
    setState((s) => ({ ...s, currentUserId: user.id }));
    return user;
  },
  logout() {
    setState((s) => ({ ...s, currentUserId: null }));
  },
  current(): User | null {
    return state.users.find((u) => u.id === state.currentUserId) ?? null;
  },
};

export const actions = {
  createStudentAccount(input: { email: string; tempPassword: string; name: string; category: Category; intake?: string }) {
    const userId = "u-" + uid();
    const studentId = "s-" + uid();
    const newUser: User = {
      id: userId,
      email: input.email,
      password: input.tempPassword,
      role: "student",
      name: input.name,
      mustChangePassword: true,
      studentId,
    };
    const newStudent: Student = {
      id: studentId,
      userId,
      category: input.category,
      intake: input.intake,
      stage: "Stage 1 — Inquiry",
      onboardingComplete: false,
      onboardingStep: 1,
      personal: {},
      academic: {},
      certifications: {},
      professional: {},
      program: {},
      createdAt: Date.now(),
      lastActivity: Date.now(),
    };
    setState((s) => ({
      ...s,
      users: [...s.users, newUser],
      students: [...s.students, newStudent],
      payments: [
        ...s.payments,
        { id: "p-" + uid(), studentId, type: "registration", label: "Registration Fee", amount: 35000, status: "Pending" },
        { id: "p-" + uid(), studentId, type: "admission", label: "Admission Letter Fee", amount: 20000, status: "Pending" },
      ],
    }));
    return { user: newUser, student: newStudent };
  },
  createTeamAccount(input: { email: string; password: string; name: string }) {
    const newUser: User = { id: "u-" + uid(), email: input.email, password: input.password, role: "team", name: input.name };
    setState((s) => ({ ...s, users: [...s.users, newUser] }));
    return newUser;
  },
  updateStudent(id: string, patch: Partial<Student>) {
    setState((s) => ({
      ...s,
      students: s.students.map((st) => (st.id === id ? { ...st, ...patch, lastActivity: Date.now() } : st)),
    }));
  },
  completeOnboarding(studentId: string, agreement: { signature: string; html: string }) {
    const student = state.students.find((s) => s.id === studentId);
    if (!student) return;
    const updated: Student = {
      ...student,
      onboardingComplete: true,
      onboardingStep: 3,
      agreement: { acceptedAt: new Date().toISOString(), ...agreement },
      lastActivity: Date.now(),
    };
    const docs = buildDocumentList(updated).map((d) => ({ ...d, id: "d-" + uid(), studentId, updatedAt: Date.now() }));
    setState((s) => ({
      ...s,
      students: s.students.map((st) => (st.id === studentId ? updated : st)),
      docs: [...s.docs.filter((d) => d.studentId !== studentId), ...docs],
      users: s.users.map((u) => (u.studentId === studentId ? { ...u, mustChangePassword: false } : u)),
    }));
  },
  uploadDoc(docId: string, fileName: string, dataUrl: string) {
    setState((s) => ({
      ...s,
      docs: s.docs.map((d) => (d.id === docId ? { ...d, fileName, dataUrl, status: "Uploaded", updatedAt: Date.now() } : d)),
    }));
  },
  setDocStatus(docId: string, status: DocStatus, notes?: string) {
    setState((s) => ({
      ...s,
      docs: s.docs.map((d) => (d.id === docId ? { ...d, status, notes: notes ?? d.notes, updatedAt: Date.now() } : d)),
    }));
  },
  assignStudent(studentId: string, teamId: string | undefined) {
    setState((s) => ({
      ...s,
      students: s.students.map((st) => (st.id === studentId ? { ...st, assignedTeamId: teamId } : st)),
    }));
  },
  addNote(studentId: string, authorId: string, authorName: string, text: string) {
    setState((s) => ({
      ...s,
      notes: [...s.notes, { id: "n-" + uid(), studentId, authorId, authorName, text, createdAt: Date.now() }],
    }));
  },
  setPaymentStatus(paymentId: string, status: "Pending" | "Paid") {
    setState((s) => ({
      ...s,
      payments: s.payments.map((p) => (p.id === paymentId ? { ...p, status, paidAt: status === "Paid" ? Date.now() : undefined } : p)),
    }));
  },
};

export { renderAgreement };
