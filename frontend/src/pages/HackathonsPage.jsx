import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card";
import { Rocket } from "lucide-react";
export default function HackathonsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Hackathon Agent</h1>
        <p className="text-muted-foreground mt-1">Discover and register for technical events.</p>
      </div>
      <Card>
        <CardHeader><CardTitle className="flex items-center gap-2"><Rocket className="h-5 w-5" /> Upcoming Events</CardTitle></CardHeader>
        <CardContent><p className="text-muted-foreground">Hackathon module integrated.</p></CardContent>
      </Card>
    </div>
  );
}
