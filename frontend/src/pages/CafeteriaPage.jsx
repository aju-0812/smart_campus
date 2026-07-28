import { useQuery } from "@tanstack/react-query";
import { apiFetch } from "../lib/api";
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card";
import { Coffee } from "lucide-react";

export default function CafeteriaPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Cafeteria Agent</h1>
        <p className="text-muted-foreground mt-1">Smart food ordering and recommendations.</p>
      </div>
      <Card>
        <CardHeader><CardTitle className="flex items-center gap-2"><Coffee className="h-5 w-5" /> Today's Menu</CardTitle></CardHeader>
        <CardContent><p className="text-muted-foreground">Cafeteria module integrated.</p></CardContent>
      </Card>
    </div>
  );
}
