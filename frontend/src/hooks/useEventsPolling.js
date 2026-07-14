import { useEffect, useState, useRef } from "react";
import axios from "axios";

const POLL_INTERVAL_MS = 15000; // 15 seconds

export function useEventsPolling(username) {
  const [events, setEvents] = useState([]);
  const [connected, setConnected] = useState(false);
  const seenIds = useRef(new Set());

  useEffect(() => {
    if (!username) return;

    setEvents([]);
    seenIds.current = new Set();
    let cancelled = false;
    let intervalId;

    const fetchEvents = async () => {
      try {
        const res = await axios.get(
          `${import.meta.env.VITE_API_URL}/api/user/${username}/events`
        );
        if (cancelled) return;

        setConnected(true);
        const fresh = res.data;

        setEvents((prev) => {
          const newOnes = fresh.filter((e) => !seenIds.current.has(e.id));
          newOnes.forEach((e) => seenIds.current.add(e.id));
          const merged = [...fresh].sort(
            (a, b) => new Date(b.created_at) - new Date(a.created_at)
          );
          return merged.slice(0, 30);
        });
      } catch (err) {
        if (!cancelled) setConnected(false);
      }
    };

    fetchEvents(); // fetch immediately on mount / username change
    intervalId = setInterval(fetchEvents, POLL_INTERVAL_MS);

    return () => {
      cancelled = true;
      clearInterval(intervalId);
    };
  }, [username]);

  return { events, connected };
}