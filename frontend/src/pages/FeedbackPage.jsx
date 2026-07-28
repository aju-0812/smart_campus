import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card";
import { MessageSquare } from "lucide-react";
export default function FeedbackPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Feedback Agent</h1>
        <p className="text-muted-foreground mt-1">NLP-powered sentiment analysis.</p>
      </div>
      <Card>
        <CardHeader><CardTitle className="flex items-center gap-2"><MessageSquare className="h-5 w-5" /> Submit Feedback</CardTitle></CardHeader>
        <CardContent><p className="text-muted-foreground">Feedback module integrated.</p></CardContent>
      </Card>
    </div>
  );
}
