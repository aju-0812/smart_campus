import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card";
import { Settings } from "lucide-react";
export default function SettingsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Settings</h1>
        <p className="text-muted-foreground mt-1">Manage your account preferences.</p>
      </div>
      <Card>
        <CardHeader><CardTitle className="flex items-center gap-2"><Settings className="h-5 w-5" /> Preferences</CardTitle></CardHeader>
        <CardContent><p className="text-muted-foreground">Settings module integrated.</p></CardContent>
      </Card>
    </div>
  );
}
