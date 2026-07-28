import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card";
import { Briefcase } from "lucide-react";
export default function PlacementPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Placement Agent</h1>
        <p className="text-muted-foreground mt-1">Career guidance and interview preparation.</p>
      </div>
      <Card>
        <CardHeader><CardTitle className="flex items-center gap-2"><Briefcase className="h-5 w-5" /> Career Profile</CardTitle></CardHeader>
        <CardContent><p className="text-muted-foreground">Placement module integrated.</p></CardContent>
      </Card>
    </div>
  );
}
